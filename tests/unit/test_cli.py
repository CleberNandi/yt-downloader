"""Unit tests for the CLI commands."""

from unittest.mock import patch

from typer.testing import CliRunner

from yt_downloader.cli import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Modern YouTube video, audio, and playlist downloader." in result.output


def test_cli_video_help():
    result = runner.invoke(app, ["video", "--help"])
    assert result.exit_code == 0
    assert "Download a single YouTube video" in result.output


def test_cli_audio_help():
    result = runner.invoke(app, ["audio", "--help"])
    assert result.exit_code == 0
    assert "Download audio only" in result.output


def test_cli_playlist_help():
    result = runner.invoke(app, ["playlist", "--help"])
    assert result.exit_code == 0
    assert "Download an entire YouTube playlist" in result.output


@patch("yt_downloader.cli._execute_download")
def test_cli_video_execution(mock_exec):
    url = "https://www.youtube.com/watch?v=sample123"
    result = runner.invoke(app, ["video", url, "--resolution", "1080"])
    assert result.exit_code == 0
    assert mock_exec.called
    options = mock_exec.call_args[0][0]
    assert options.url == url
    assert options.video_resolution.value == "1080"


@patch("yt_downloader.cli._execute_download")
def test_cli_audio_execution(mock_exec):
    url = "https://www.youtube.com/watch?v=sample123"
    result = runner.invoke(app, ["audio", url, "--quality", "320", "--format", "mp3"])
    assert result.exit_code == 0
    assert mock_exec.called
    options = mock_exec.call_args[0][0]
    assert options.url == url
    assert options.audio_quality.value == "320"
    assert options.audio_format.value == "mp3"


@patch("yt_downloader.cli._execute_download")
def test_cli_video_execution_verbose(mock_exec):
    url = "https://www.youtube.com/watch?v=sample123"
    result = runner.invoke(app, ["video", url, "--verbose"])
    assert result.exit_code == 0
    assert mock_exec.called
    options = mock_exec.call_args[0][0]
    assert options.verbose is True
