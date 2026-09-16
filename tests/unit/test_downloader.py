"""Unit tests for Downloader engine using mocks."""

from unittest.mock import MagicMock, patch

from yt_dlp.utils import DownloadError

from yt_downloader.core.downloader import Downloader
from yt_downloader.core.models import (
    AudioFormat,
    AudioQuality,
    DownloadOptions,
    DownloadType,
    VideoResolution,
)


def test_build_ydl_opts_audio(tmp_path):
    options = DownloadOptions(
        url="https://www.youtube.com/watch?v=mock123",
        download_type=DownloadType.AUDIO,
        output_dir=tmp_path,
        audio_quality=AudioQuality.Q320,
        audio_format=AudioFormat.MP3,
        embed_thumbnail=True,
        embed_metadata=True,
    )
    downloader = Downloader(options)
    opts = downloader.build_ydl_opts()

    assert opts["format"] == "bestaudio/best"
    assert opts["noplaylist"] is True
    assert "writethumbnail" in opts

    postprocessor_keys = [p["key"] for p in opts.get("postprocessors", [])]
    assert "FFmpegExtractAudio" in postprocessor_keys
    assert "FFmpegMetadata" in postprocessor_keys
    assert "FFmpegThumbnailsConvertor" in postprocessor_keys
    assert "EmbedThumbnail" in postprocessor_keys
    assert postprocessor_keys.index("FFmpegThumbnailsConvertor") < postprocessor_keys.index(
        "EmbedThumbnail"
    )


def test_build_ydl_opts_video(tmp_path):
    options = DownloadOptions(
        url="https://www.youtube.com/watch?v=mock123",
        download_type=DownloadType.VIDEO,
        output_dir=tmp_path,
        video_resolution=VideoResolution.P1080,
    )
    downloader = Downloader(options)
    opts = downloader.build_ydl_opts()

    assert "1080" in opts["format"]
    assert opts["merge_output_format"] == "mp4"
    assert opts["noplaylist"] is True


def test_build_ydl_opts_playlist(tmp_path):
    options = DownloadOptions(
        url="https://www.youtube.com/playlist?list=mock123",
        download_type=DownloadType.PLAYLIST,
        output_dir=tmp_path,
        is_playlist=True,
    )
    downloader = Downloader(options)
    opts = downloader.build_ydl_opts()

    assert opts["noplaylist"] is False
    assert "%(playlist_title)s" in opts["outtmpl"]


@patch("yt_downloader.core.downloader.YoutubeDL")
def test_download_success(mock_ytdl_class, tmp_path):
    mock_instance = MagicMock()
    mock_instance.extract_info.return_value = {"title": "Test Video Title"}
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    options = DownloadOptions(
        url="https://www.youtube.com/watch?v=mock123",
        download_type=DownloadType.VIDEO,
        output_dir=tmp_path,
    )
    downloader = Downloader(options)
    result = downloader.download()

    assert result.success is True
    assert result.title == "Test Video Title"
    mock_instance.extract_info.assert_called_once_with(options.url, download=True)


@patch("yt_downloader.core.downloader.YoutubeDL")
def test_download_failure(mock_ytdl_class, tmp_path):
    mock_instance = MagicMock()
    mock_instance.extract_info.side_effect = DownloadError("Video unavailable")
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    options = DownloadOptions(
        url="https://www.youtube.com/watch?v=mock123",
        download_type=DownloadType.VIDEO,
        output_dir=tmp_path,
    )
    downloader = Downloader(options)
    result = downloader.download()

    assert result.success is False
    assert "YouTube download error" in (result.error_message or "")
