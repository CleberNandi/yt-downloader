"""Rich-styled banner and header presentation with solid typography."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from yt_downloader import __version__

ASCII_ART = r"""
  ██╗   ██╗████████╗     ██████╗  ██████╗ ██╗    ██╗███╗   ██╗
  ╚██╗ ██╔╝╚══██╔══╝     ██╔══██╗██╔═══██╗██║    ██║████╗  ██║
   ╚████╔╝    ██║        ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║
    ╚██╔╝     ██║        ██║  ██║██║   ██║██║███╗██║██║╚██╗██║
     ██║      ██║        ██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║
     ╚═╝      ╚═╝        ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
"""


def render_banner(console: Console) -> None:
    """Renders a stylish header banner in the terminal with filled typography."""
    txt = Text()
    txt.append(ASCII_ART, style="bold cyan")
    txt.append(
        f"     ⚡ yt-downloader • Python 3.14 • yt-dlp • FFmpeg • v{__version__}\n",
        style="bold white",
    )

    panel = Panel(
        txt,
        border_style="bold cyan",
        style="on #1e1e2e",
        expand=False,
        padding=(0, 2),
    )
    console.print(panel)
