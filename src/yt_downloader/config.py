"""Configuration and path management for yt-downloader."""

import os
import shutil
from pathlib import Path


def get_base_download_dir() -> Path:
    """Returns the base download directory, respecting environment variable if set."""
    env_dir = os.getenv("YTDL_DOWNLOAD_DIR")
    if env_dir:
        return Path(env_dir).expanduser().resolve()
    return Path.home() / "Downloads" / "yt-downloader"


def get_output_dir(subfolder: str | None = None, custom_dir: Path | str | None = None) -> Path:
    """Returns the target directory for downloads, ensuring it exists."""
    if custom_dir:
        target = Path(custom_dir).expanduser().resolve()
    else:
        base = get_base_download_dir()
        target = base / subfolder if subfolder else base

    target.mkdir(parents=True, exist_ok=True)
    return target


def has_ffmpeg() -> bool:
    """Checks whether ffmpeg executable is available in PATH."""
    return shutil.which("ffmpeg") is not None
