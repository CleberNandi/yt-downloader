# pyright: reportPrivateImportUsage=false
"""Interactive prompts and selection menus powered by InquirerPy."""

import sys
from collections.abc import Callable

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator

from yt_downloader.core.models import (
    AudioFormat,
    AudioQuality,
    VideoResolution,
)


def _safe_execute[T](func: Callable[[], T]) -> T:
    """Executes an interactive prompt safely, intercepting KeyboardInterrupt / Esc."""
    try:
        result = func()
        if result is None:
            print("\nOperação cancelada pelo usuário.")
            sys.exit(0)
        return result
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
        sys.exit(0)


def prompt_download_type() -> str:
    """Prompts for download type using arrow keys, numbers or fuzzy text."""
    return _safe_execute(
        lambda: inquirer.fuzzy(
            message="O que você deseja baixar?",
            choices=[
                Choice(value="audio", name="1) 🎵 Áudio / Música (MP3 com tags e capa)"),
                Choice(value="video", name="2) 🎬 Vídeo (MP4 em alta definição)"),
                Choice(value="playlist", name="3) 📑 Playlist Completa"),
                Choice(value="exit", name="4) 🚪 Sair"),
            ],
            default="",
            pointer="❯ ",
            prompt="",
            info=False,
            instruction="(↑/↓ navegar • digite número ou texto • Enter confirma)",
        ).execute()
    )


def prompt_youtube_url() -> str:
    """Prompts for YouTube URL with inline validation."""

    def validate_url(text: str) -> bool:
        clean = text.strip()
        if not clean:
            return False
        return "youtube.com" in clean or "youtu.be" in clean or clean.startswith("http")

    return _safe_execute(
        lambda: inquirer.text(
            message="Insira a URL do YouTube:",
            validate=EmptyInputValidator("A URL não pode estar vazia."),
            invalid_message="Por favor, insira uma URL válida do YouTube.",
            transformer=lambda result: result.strip(),
            filter=lambda result: result.strip(),
        ).execute()
    )


def prompt_video_resolution() -> VideoResolution:
    """Prompts for target video resolution."""
    return _safe_execute(
        lambda: inquirer.fuzzy(
            message="Selecione a resolução máxima desejada:",
            choices=[
                Choice(value=VideoResolution.BEST, name="1) 🌟 Melhor Disponível (Best / 4K)"),
                Choice(value=VideoResolution.P1080, name="2) 📺 1080p (Full HD)"),
                Choice(value=VideoResolution.P720, name="3) 📱 720p (HD)"),
                Choice(value=VideoResolution.P480, name="4) 💾 480p (SD / Baixo consumo)"),
            ],
            default="",
            pointer="❯ ",
            prompt="",
            info=False,
            instruction="(↑/↓ navegar • digite número ou texto • Enter confirma)",
        ).execute()
    )


def prompt_audio_quality() -> AudioQuality:
    """Prompts for audio bitrate quality."""
    return _safe_execute(
        lambda: inquirer.fuzzy(
            message="Selecione a qualidade do áudio:",
            choices=[
                Choice(value=AudioQuality.Q320, name="1) 💎 320 kbps (Alta fidelidade)"),
                Choice(value=AudioQuality.Q256, name="2) 🎧 256 kbps (Muito boa)"),
                Choice(value=AudioQuality.Q192, name="3) 📻 192 kbps (Padrão)"),
                Choice(value=AudioQuality.Q128, name="4) 📦 128 kbps (Econômico)"),
                Choice(value=AudioQuality.BEST, name="5) 🎛️ VBR Best (Taxa variável)"),
            ],
            default="",
            pointer="❯ ",
            prompt="",
            info=False,
            instruction="(↑/↓ navegar • digite número ou texto • Enter confirma)",
        ).execute()
    )


def prompt_audio_format() -> AudioFormat:
    """Prompts for output audio format."""
    return _safe_execute(
        lambda: inquirer.fuzzy(
            message="Selecione o formato de áudio:",
            choices=[
                Choice(value=AudioFormat.MP3, name="1) MP3 (Compatível com qualquer reprodutor)"),
                Choice(value=AudioFormat.M4A, name="2) M4A / AAC (Ótimo para dispositivos Apple)"),
                Choice(value=AudioFormat.FLAC, name="3) FLAC (Lossless de estúdio)"),
                Choice(value=AudioFormat.OPUS, name="4) OPUS (Codec nativo do YouTube)"),
            ],
            default="",
            pointer="❯ ",
            prompt="",
            info=False,
            instruction="(↑/↓ navegar • digite número ou texto • Enter confirma)",
        ).execute()
    )


def prompt_playlist_mode() -> bool:
    """Prompts whether playlist should be downloaded as audio or video."""
    return _safe_execute(
        lambda: inquirer.fuzzy(
            message="Como deseja baixar os itens da playlist?",
            choices=[
                Choice(value=True, name="1) 🎵 Áudio (MP3 para cada música com capa)"),
                Choice(value=False, name="2) 🎬 Vídeo (MP4 para cada vídeo)"),
            ],
            default="",
            pointer="❯ ",
            prompt="",
            info=False,
            instruction="(↑/↓ navegar • digite número ou texto • Enter confirma)",
        ).execute()
    )
