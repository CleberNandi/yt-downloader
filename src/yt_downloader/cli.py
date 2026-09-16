"""Command-line interface for yt-downloader powered by Typer and Rich."""

from pathlib import Path
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.prompt import Confirm, Prompt

from yt_downloader.config import has_ffmpeg
from yt_downloader.core.downloader import Downloader
from yt_downloader.core.models import (
    AudioFormat,
    AudioQuality,
    DownloadOptions,
    DownloadType,
    VideoResolution,
)

app = typer.Typer(
    name="ytdl",
    help="Modern YouTube video, audio, and playlist downloader.",
    add_completion=False,
    no_args_is_help=False,
)

console = Console()


def _check_system_ffmpeg() -> None:
    """Displays a warning if ffmpeg is not installed."""
    if not has_ffmpeg():
        console.print(
            "[yellow]Warning: FFmpeg was not found in your PATH.[/yellow]\n"
            "[dim]Audio conversion to MP3 and video/audio merging require FFmpeg.[/dim]\n"
        )


def _execute_download(options: DownloadOptions) -> None:
    """Runs the downloader with rich visual feedback."""
    _check_system_ffmpeg()
    downloader = Downloader(options)

    with Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task_id = progress.add_task("Downloading...", total=None)

        def progress_hook(d: dict[str, Any]) -> None:
            if d.get("status") == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate")
                downloaded = d.get("downloaded_bytes", 0)
                if total:
                    progress.update(task_id, total=total, completed=downloaded)
                else:
                    progress.update(task_id, completed=downloaded)
            elif d.get("status") == "finished":
                progress.update(task_id, description="[bold green]Processing & Merging...")

        result = downloader.download(progress_hook=progress_hook)

    if result.success:
        title = result.title or options.url
        console.print(
            Panel.fit(
                f"[bold green]✓ Download finished successfully![/bold green]\n\n"
                f"[bold]Title:[/bold] {title}\n"
                f"[bold]Destination:[/bold] {downloader._resolve_output_dir()}",
                title="yt-downloader",
                border_style="green",
            )
        )
    else:
        console.print(
            Panel.fit(
                f"[bold red]✗ Download failed![/bold red]\n\n[red]{result.error_message}[/red]",
                title="Error",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)


@app.command("video")
def download_video(
    url: Annotated[str, typer.Argument(help="YouTube video URL")],
    resolution: Annotated[
        VideoResolution,
        typer.Option("--resolution", "-r", help="Maximum video resolution"),
    ] = VideoResolution.BEST,
    output_dir: Annotated[
        Path | None,
        typer.Option("--output-dir", "-o", help="Custom output directory"),
    ] = None,
    cookies: Annotated[
        str | None,
        typer.Option("--cookies", "-c", help="Browser cookies (e.g. firefox, chrome)"),
    ] = None,
    no_thumbnail: Annotated[
        bool,
        typer.Option("--no-thumbnail", help="Do not embed video thumbnail"),
    ] = False,
    no_metadata: Annotated[
        bool,
        typer.Option("--no-metadata", help="Do not embed video metadata"),
    ] = False,
) -> None:
    """Download a single YouTube video with best merged audio/video."""
    options = DownloadOptions(
        url=url,
        download_type=DownloadType.VIDEO,
        output_dir=output_dir,
        video_resolution=resolution,
        embed_thumbnail=not no_thumbnail,
        embed_metadata=not no_metadata,
        cookies_from_browser=cookies,
    )
    _execute_download(options)


@app.command("audio")
def download_audio(
    url: Annotated[str, typer.Argument(help="YouTube video or music URL")],
    quality: Annotated[
        AudioQuality,
        typer.Option("--quality", "-q", help="Audio bitrate quality (kbps)"),
    ] = AudioQuality.Q320,
    audio_format: Annotated[
        AudioFormat,
        typer.Option("--format", "-f", help="Output audio format"),
    ] = AudioFormat.MP3,
    output_dir: Annotated[
        Path | None,
        typer.Option("--output-dir", "-o", help="Custom output directory"),
    ] = None,
    cookies: Annotated[
        str | None,
        typer.Option("--cookies", "-c", help="Browser cookies (e.g. firefox, chrome)"),
    ] = None,
    no_thumbnail: Annotated[
        bool,
        typer.Option("--no-thumbnail", help="Do not embed cover art thumbnail"),
    ] = False,
    no_metadata: Annotated[
        bool,
        typer.Option("--no-metadata", help="Do not embed audio ID3 tags"),
    ] = False,
) -> None:
    """Download audio only (music/clips) converted to MP3/M4A with ID3 tags & cover art."""
    options = DownloadOptions(
        url=url,
        download_type=DownloadType.AUDIO,
        output_dir=output_dir,
        audio_quality=quality,
        audio_format=audio_format,
        embed_thumbnail=not no_thumbnail,
        embed_metadata=not no_metadata,
        cookies_from_browser=cookies,
    )
    _execute_download(options)


@app.command("playlist")
def download_playlist(
    url: Annotated[str, typer.Argument(help="YouTube playlist URL")],
    audio_only: Annotated[
        bool,
        typer.Option("--audio", "-a", help="Download playlist items as audio (MP3)"),
    ] = False,
    items: Annotated[
        str | None,
        typer.Option("--items", help="Playlist items to download (e.g. 1-5, 10)"),
    ] = None,
    output_dir: Annotated[
        Path | None,
        typer.Option("--output-dir", "-o", help="Custom output directory"),
    ] = None,
    cookies: Annotated[
        str | None,
        typer.Option("--cookies", "-c", help="Extract cookies from browser"),
    ] = None,
) -> None:
    """Download an entire YouTube playlist (video or audio-only)."""
    options = DownloadOptions(
        url=url,
        download_type=DownloadType.AUDIO if audio_only else DownloadType.PLAYLIST,
        output_dir=output_dir,
        is_playlist=True,
        playlist_items=items,
        cookies_from_browser=cookies,
    )
    _execute_download(options)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Default entrypoint: launches interactive prompt if no command is given."""
    if ctx.invoked_subcommand is not None:
        return

    console.print(
        Panel.fit(
            "[bold cyan]yt-downloader[/bold cyan] — Modern YouTube Downloader\n"
            "[dim]Python 3.14 • uv • yt-dlp • FFmpeg[/dim]",
            border_style="cyan",
        )
    )

    choice = Prompt.ask(
        "\nWhat would you like to download?",
        choices=["video", "audio", "playlist", "exit"],
        default="audio",
    )

    if choice == "exit":
        raise typer.Exit()

    url = Prompt.ask("Enter YouTube URL").strip()
    if not url:
        console.print("[red]URL cannot be empty.[/red]")
        raise typer.Exit(code=1)

    match choice:
        case "audio":
            quality = Prompt.ask(
                "Select Audio Quality (kbps)",
                choices=["320", "256", "192", "128", "0"],
                default="320",
            )
            options = DownloadOptions(
                url=url,
                download_type=DownloadType.AUDIO,
                audio_quality=AudioQuality(quality),
            )
        case "video":
            res = Prompt.ask(
                "Select Resolution",
                choices=["best", "1080", "720", "480"],
                default="best",
            )
            options = DownloadOptions(
                url=url,
                download_type=DownloadType.VIDEO,
                video_resolution=VideoResolution(res),
            )
        case "playlist":
            is_audio = Confirm.ask("Download playlist as Audio (MP3)?", default=True)
            options = DownloadOptions(
                url=url,
                download_type=DownloadType.AUDIO if is_audio else DownloadType.PLAYLIST,
                is_playlist=True,
            )
        case _:
            raise typer.Exit(code=1)

    _execute_download(options)


if __name__ == "__main__":
    app()
