"""Logging configuration and yt-dlp logger adapter for yt-downloader."""

import logging
import re
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOGGER_NAME = "yt_downloader"
LOG_DIR = Path.cwd() / "logs"
LOG_FILE = LOG_DIR / "ytdl.log"

ANSI_REGEX = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]|\x1b\].*?\x07")


def _strip_ansi(text: str) -> str:
    """Removes ANSI terminal escape sequences."""
    return ANSI_REGEX.sub("", text).strip()


def _is_progress_tick(msg: str) -> bool:
    """Identifies noisy per-frame/fragment download progress ticks."""
    if "ETA" in msg or "(frag " in msg:
        return True
    if msg.startswith("[download]") and "%" in msg and " in " not in msg:
        return True
    speed_units = ("KiB/s", "MiB/s", "GiB/s", "B/s")
    return "%" in msg and any(unit in msg for unit in speed_units) and " in " not in msg


class YTDLLogger:
    """Adapter that redirects yt-dlp internal messages to Python standard logging."""

    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    def debug(self, msg: str) -> None:
        clean = _strip_ansi(msg)
        if not clean or _is_progress_tick(clean):
            return
        self._logger.debug(clean)

    def info(self, msg: str) -> None:
        clean = _strip_ansi(msg)
        if not clean or _is_progress_tick(clean):
            return
        self._logger.info(clean)

    def warning(self, msg: str) -> None:
        clean = _strip_ansi(msg)
        if clean:
            self._logger.warning(clean)

    def error(self, msg: str) -> None:
        clean = _strip_ansi(msg)
        if clean:
            self._logger.error(clean)


def setup_logging(verbose: bool = False, log_file: Path | None = None) -> logging.Logger:
    """Configures application logger with RotatingFileHandler and optional console handler."""
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers if setup is called multiple times
    if logger.handlers:
        return logger

    target_log_file = log_file or LOG_FILE
    target_log_file.parent.mkdir(parents=True, exist_ok=True)

    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Rotating file handler: 5MB per file, up to 3 backups
    file_handler = RotatingFileHandler(
        target_log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    if verbose:
        console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger


def get_logger() -> logging.Logger:
    """Returns the main application logger."""
    return logging.getLogger(LOGGER_NAME)
