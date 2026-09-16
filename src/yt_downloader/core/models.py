"""Data models and enums for yt-downloader."""

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class DownloadType(StrEnum):
    """Supported download types."""

    VIDEO = "video"
    AUDIO = "audio"
    PLAYLIST = "playlist"


class AudioQuality(StrEnum):
    """Audio bitrates in kbps."""

    BEST = "0"  # VBR best
    Q320 = "320"
    Q256 = "256"
    Q192 = "192"
    Q128 = "128"


class AudioFormat(StrEnum):
    """Audio output formats."""

    MP3 = "mp3"
    M4A = "m4a"
    FLAC = "flac"
    OPUS = "opus"


class VideoResolution(StrEnum):
    """Maximum target video resolution height."""

    BEST = "best"
    P2160 = "2160"  # 4K
    P1440 = "1440"  # 2K
    P1080 = "1080"  # FHD
    P720 = "720"  # HD
    P480 = "480"  # SD


@dataclass
class DownloadOptions:
    """Configuration options for a download task."""

    url: str
    download_type: DownloadType = DownloadType.VIDEO
    output_dir: Path | None = None
    audio_quality: AudioQuality = AudioQuality.Q320
    audio_format: AudioFormat = AudioFormat.MP3
    video_resolution: VideoResolution = VideoResolution.BEST
    embed_thumbnail: bool = True
    embed_metadata: bool = True
    cookies_from_browser: str | None = None
    is_playlist: bool = False
    playlist_items: str | None = None
    verbose: bool = False


@dataclass
class DownloadResult:
    """Result of a download task."""

    success: bool
    title: str | None = None
    file_paths: list[Path] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    error_message: str | None = None
