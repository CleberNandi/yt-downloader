"""Rich-styled banner and header presentation with solid typography."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from yt_downloader import __version__

ASCII_LINES = [
    "  ██╗   ██╗████████╗     ██████╗  ██████╗ ██╗    ██╗███╗   ██╗",
    "  ╚██╗ ██╔╝╚══██╔══╝     ██╔══██╗██╔═══██╗██║    ██║████╗  ██║",
    "   ╚████╔╝    ██║        ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║",
    "    ╚██╔╝     ██║        ██║  ██║██║   ██║██║███╗██║██║╚██╗██║",
    "     ██║      ██║        ██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║",
    "     ╚═╝      ╚═╝        ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝",
]
ART_WIDTH = 62
ASCII_ART = "\n".join(ASCII_LINES)


def render_banner(console: Console) -> None:
    """Renders a stylish header banner in the terminal with 3D shadow typography."""
    subtitle = f"● yt-downloader • Python 3.14 • yt-dlp • FFmpeg • v{__version__}"

    txt = Text()
    txt.append(ASCII_ART + "\n\n", style="bold cyan")
    txt.append(subtitle.center(ART_WIDTH) + "\n", style="bold white")

    panel = Panel(
        txt,
        border_style="bold cyan",
        expand=False,
        padding=(0, 2),
    )
    console.print(panel)
