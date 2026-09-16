"""Unit tests for config and path helpers."""

from pathlib import Path
from unittest.mock import patch

from yt_downloader.config import get_base_download_dir, get_output_dir, has_ffmpeg


def test_get_base_download_dir_default(monkeypatch):
    monkeypatch.delenv("YTDL_DOWNLOAD_DIR", raising=False)
    expected = Path.home() / "Downloads" / "yt-downloader"
    assert get_base_download_dir() == expected


def test_get_base_download_dir_env(monkeypatch, tmp_path):
    custom = tmp_path / "custom_downloads"
    monkeypatch.setenv("YTDL_DOWNLOAD_DIR", str(custom))
    assert get_base_download_dir() == custom.resolve()


def test_get_output_dir_creates_subfolder(tmp_path, monkeypatch):
    monkeypatch.setenv("YTDL_DOWNLOAD_DIR", str(tmp_path))
    audio_dir = get_output_dir(subfolder="audio")
    assert audio_dir.exists()
    assert audio_dir.is_dir()
    assert audio_dir.name == "audio"


def test_get_output_dir_custom_dir(tmp_path):
    custom_target = tmp_path / "explicit_dir"
    result = get_output_dir(custom_dir=custom_target)
    assert result.exists()
    assert result == custom_target.resolve()


def test_has_ffmpeg():
    with patch("shutil.which", return_value="/usr/bin/ffmpeg"):
        assert has_ffmpeg() is True
    with patch("shutil.which", return_value=None):
        assert has_ffmpeg() is False
