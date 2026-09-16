"""Unit tests for UI components, banner and interactive prompts."""

from unittest.mock import MagicMock, patch

import pytest
from rich.console import Console

from yt_downloader.core.models import AudioFormat, AudioQuality, VideoResolution
from yt_downloader.ui.banner import render_banner
from yt_downloader.ui.prompts import (
    _safe_execute,
    prompt_audio_format,
    prompt_audio_quality,
    prompt_download_type,
    prompt_playlist_mode,
    prompt_video_resolution,
    prompt_youtube_url,
)


def test_render_banner():
    console = Console(record=True)
    render_banner(console)
    output = console.export_text()
    assert "Python 3.14" in output
    assert "yt-dlp" in output
    assert "FFmpeg" in output


def test_safe_execute_success():
    assert _safe_execute(lambda: "ok") == "ok"


def test_safe_execute_keyboard_interrupt():
    def raise_interrupt():
        raise KeyboardInterrupt()

    with pytest.raises(SystemExit) as exc:
        _safe_execute(raise_interrupt)
    assert exc.value.code == 0


@patch("InquirerPy.inquirer.select")
def test_prompt_download_type(mock_select):
    mock_instance = MagicMock()
    mock_instance.execute.return_value = "audio"
    mock_select.return_value = mock_instance

    result = prompt_download_type()
    assert result == "audio"


@patch("InquirerPy.inquirer.text")
def test_prompt_youtube_url(mock_text):
    mock_instance = MagicMock()
    mock_instance.execute.return_value = "https://www.youtube.com/watch?v=123"
    mock_text.return_value = mock_instance

    result = prompt_youtube_url()
    assert result == "https://www.youtube.com/watch?v=123"


@patch("InquirerPy.inquirer.select")
def test_prompt_video_resolution(mock_select):
    mock_instance = MagicMock()
    mock_instance.execute.return_value = VideoResolution.P1080
    mock_select.return_value = mock_instance

    result = prompt_video_resolution()
    assert result == VideoResolution.P1080


@patch("InquirerPy.inquirer.select")
def test_prompt_audio_quality(mock_select):
    mock_instance = MagicMock()
    mock_instance.execute.return_value = AudioQuality.Q320
    mock_select.return_value = mock_instance

    result = prompt_audio_quality()
    assert result == AudioQuality.Q320


@patch("InquirerPy.inquirer.select")
def test_prompt_audio_format(mock_select):
    mock_instance = MagicMock()
    mock_instance.execute.return_value = AudioFormat.MP3
    mock_select.return_value = mock_instance

    result = prompt_audio_format()
    assert result == AudioFormat.MP3


@patch("InquirerPy.inquirer.select")
def test_prompt_playlist_mode(mock_select):
    mock_instance = MagicMock()
    mock_instance.execute.return_value = True
    mock_select.return_value = mock_instance

    assert prompt_playlist_mode() is True
