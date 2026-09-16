"""Rich-styled banner and header presentation."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from yt_downloader import __version__

ASCII_ART = r"""
 __   _______     ____                        _                 _
 \ \ / /_   _|   |  _ \  _____      ___ __   | | ___   __ _  __| |
  \ V /  | |_____| | | |/ _ \ \ /\ / / '_ \  | |/ _ \ / _` |/ _` |
   | |   | |_____| |_| | (_) \ V  V /| | | | | | (_) | (_| | (_| |
   |_|   |_|     |____/ \___/ \_/\_/ |_| |_| |_|\___/ \__,_|\__,_|
"""


def render_banner(console: Console) -> None:
    """Renders a stylish header banner in the terminal."""
    logo = Text(ASCII_ART, style="bold cyan")
    info = Text(
        f"\n  Python 3.14  •  uv  •  yt-dlp  •  FFmpeg  •  v{__version__}\n",
        style="dim white",
    )
    banner_content = Text.assemble(logo, info)
    console.print(
        Panel(
            banner_content,
            border_style="cyan",
            expand=False,
            padding=(0, 2),
        )
    )
