"""High-level download engine wrapping yt-dlp."""

from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from yt_downloader.config import get_output_dir
from yt_downloader.core.models import (
    DownloadOptions,
    DownloadResult,
    DownloadType,
    VideoResolution,
)
from yt_downloader.logger import YTDLLogger, get_logger


class Downloader:
    """Orchestrates YouTube downloads using yt-dlp."""

    def __init__(self, options: DownloadOptions) -> None:
        self.options = options

    def _resolve_output_dir(self) -> Path:
        if self.options.output_dir:
            return get_output_dir(custom_dir=self.options.output_dir)

        match self.options.download_type:
            case DownloadType.AUDIO:
                return get_output_dir(subfolder="audio")
            case DownloadType.PLAYLIST:
                return get_output_dir(subfolder="playlists")
            case _:
                return get_output_dir(subfolder="video")

    def build_ydl_opts(
        self,
        progress_hook: Callable[[dict[str, Any]], None] | None = None,
    ) -> dict[str, Any]:
        """Constructs yt-dlp options dictionary from DownloadOptions."""
        out_dir = self._resolve_output_dir()

        if self.options.is_playlist or self.options.download_type == DownloadType.PLAYLIST:
            playlist_name = "%(playlist_title)s"
            item_name = "%(playlist_index)02d - %(title)s.%(ext)s"
            out_template = str(out_dir / playlist_name / item_name)
            noplaylist = False
        else:
            out_template = str(out_dir / "%(title)s.%(ext)s")
            noplaylist = True

        logger = get_logger()
        ydl_opts: dict[str, Any] = {
            "outtmpl": out_template,
            "noplaylist": noplaylist,
            "windowsfilenames": True,  # Clean filenames on all platforms
            "logger": YTDLLogger(logger),
        }

        if self.options.cookies_from_browser:
            ydl_opts["cookiesfrombrowser"] = (self.options.cookies_from_browser, None, None, None)

        if self.options.playlist_items:
            ydl_opts["playlist_items"] = self.options.playlist_items

        if progress_hook:
            ydl_opts["progress_hooks"] = [progress_hook]

        postprocessors: list[dict[str, Any]] = []

        if self.options.download_type == DownloadType.AUDIO:
            ydl_opts["format"] = "bestaudio/best"
            postprocessors.append(
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.options.audio_format.value,
                    "preferredquality": self.options.audio_quality.value,
                }
            )
            if self.options.embed_metadata:
                postprocessors.append({"key": "FFmpegMetadata", "add_metadata": True})
            if self.options.embed_thumbnail:
                ydl_opts["writethumbnail"] = True
                postprocessors.append({"key": "FFmpegThumbnailsConvertor", "format": "jpg"})
                postprocessors.append({"key": "EmbedThumbnail", "already_have_thumbnail": False})

        else:
            # Video configuration
            if self.options.video_resolution == VideoResolution.BEST:
                ydl_opts["format"] = "bestvideo+bestaudio/best"
            else:
                height = self.options.video_resolution.value
                ydl_opts["format"] = (
                    f"bestvideo[height<={height}]+bestaudio/best[height<={height}]/best"
                )

            ydl_opts["merge_output_format"] = "mp4"

            if self.options.embed_metadata:
                postprocessors.append({"key": "FFmpegMetadata", "add_metadata": True})
            if self.options.embed_thumbnail:
                ydl_opts["writethumbnail"] = True
                postprocessors.append({"key": "FFmpegThumbnailsConvertor", "format": "jpg"})
                postprocessors.append({"key": "EmbedThumbnail", "already_have_thumbnail": False})

        if postprocessors:
            ydl_opts["postprocessors"] = postprocessors

        return ydl_opts

    def fetch_info(self) -> dict[str, Any]:
        """Extracts video/playlist metadata without downloading."""
        opts = {"quiet": True, "extract_flat": "in_playlist"}
        if self.options.cookies_from_browser:
            opts["cookiesfrombrowser"] = (self.options.cookies_from_browser, None, None, None)
        with YoutubeDL(cast(Any, opts)) as ydl:
            info = ydl.extract_info(self.options.url, download=False)
            return dict(info) if info else {}

    def download(
        self,
        progress_hook: Callable[[dict[str, Any]], None] | None = None,
    ) -> DownloadResult:
        """Executes the download process."""
        ydl_opts = self.build_ydl_opts(progress_hook=progress_hook)
        downloaded_files: list[Path] = []

        def track_downloaded(filename: str) -> None:
            p = Path(filename)
            if p not in downloaded_files:
                downloaded_files.append(p)

        def internal_hook(d: dict[str, Any]) -> None:
            if d.get("status") == "finished":
                fn = d.get("filename")
                if fn:
                    track_downloaded(fn)
            if progress_hook:
                progress_hook(d)

        ydl_opts["progress_hooks"] = [internal_hook]

        logger = get_logger()
        logger.info(
            "Starting download for URL: %s (type: %s)",
            self.options.url,
            self.options.download_type.value,
        )

        try:
            with YoutubeDL(cast(Any, ydl_opts)) as ydl:
                info = ydl.extract_info(self.options.url, download=True)
                title = info.get("title") if info else None
                logger.info("Download completed successfully: %s", title)
                return DownloadResult(
                    success=True,
                    title=title,
                    file_paths=downloaded_files,
                )
        except Exception as err:
            existing_files = [p for p in downloaded_files if p.exists() and p.stat().st_size > 0]
            out_dir = self._resolve_output_dir()
            if not existing_files and out_dir.exists():
                recent_media = [
                    f
                    for f in out_dir.glob("*")
                    if f.is_file()
                    and f.suffix.lower() in {".mp4", ".mp3", ".m4a", ".webm", ".flac", ".opus"}
                    and f.stat().st_size > 0
                ]
                existing_files.extend(recent_media)

            if existing_files:
                logger.warning(
                    "Download succeeded with post-processing warning: %s. Output files: %s",
                    err,
                    existing_files,
                )
                return DownloadResult(
                    success=True,
                    title=existing_files[0].stem,
                    file_paths=existing_files,
                    warnings=[f"Post-processing warning: {err}"],
                )

            logger.error("Download failed completely: %s", err, exc_info=True)
            if isinstance(err, DownloadError):
                return DownloadResult(
                    success=False,
                    error_message=f"YouTube download error: {err}",
                )
            return DownloadResult(
                success=False,
                error_message=f"Unexpected error: {err}",
            )
