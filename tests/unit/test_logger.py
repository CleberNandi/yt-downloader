"""Unit tests for the logging configuration and YTDLLogger adapter."""

import logging
from unittest.mock import MagicMock

from yt_downloader.logger import YTDLLogger, setup_logging


def test_ytdl_logger_adapter():
    mock_logger = MagicMock(spec=logging.Logger)
    adapter = YTDLLogger(mock_logger)

    adapter.debug("[debug] Testing debug msg")
    mock_logger.debug.assert_called_with("[debug] Testing debug msg")

    adapter.info("Testing info msg")
    mock_logger.info.assert_called_with("Testing info msg")

    adapter.warning("Testing warning msg")
    mock_logger.warning.assert_called_with("Testing warning msg")

    adapter.error("Testing error msg")
    mock_logger.error.assert_called_with("Testing error msg")


def test_ytdl_logger_strips_ansi_and_filters_progress_ticks():
    mock_logger = MagicMock(spec=logging.Logger)
    adapter = YTDLLogger(mock_logger)

    # Progress ticks should be filtered out
    adapter.debug(
        "\x1b[0;94m 98.1%\x1b[0m of ~ 157.06MiB at \x1b[0;32m 5.29MiB/s\x1b[0m ETA 00:01 (frag 1/2)"
    )
    adapter.debug("[download]   2.5% of ~ 104.02MiB at 1.48MiB/s ETA 00:55 (frag 3/163)")
    adapter.debug("[download]  98.4% of 138.90MiB at Unknown B/s ETA Unknown")
    adapter.debug("[download]  50.0% of 100.00MiB at 10.00MiB/s")
    mock_logger.debug.assert_not_called()

    # Milestones and important messages should be kept and ANSI stripped
    adapter.debug("[download] Destination: /path/to/video.mp4")
    mock_logger.debug.assert_called_with("[download] Destination: /path/to/video.mp4")

    adapter.debug("\x1b[0;94m[download] 100% of 138.90MiB in 00:00:14 at 9.57MiB/s\x1b[0m")
    mock_logger.debug.assert_called_with("[download] 100% of 138.90MiB in 00:00:14 at 9.57MiB/s")

    adapter.warning("\x1b[0;33m[youtube] Warning message\x1b[0m")
    mock_logger.warning.assert_called_with("[youtube] Warning message")


def test_setup_logging(tmp_path):
    log_file = tmp_path / "custom_logs" / "test.log"
    logger = setup_logging(verbose=False, log_file=log_file)

    assert logger.name == "yt_downloader"
    assert log_file.parent.exists()

    logger.info("Hello test log file")
    for handler in logger.handlers:
        handler.flush()

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "Hello test log file" in content
