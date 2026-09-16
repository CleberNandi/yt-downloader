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
