# yt-downloader 🎬🎵

[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Modern, reliable, and high-performance YouTube downloader for Videos, Playlists, and High-Fidelity Audio extraction (MP3 with ID3 tags and cover art). Built with **Python 3.14**, **uv**, **yt-dlp**, **Typer**, and **Rich**.

---

## ✨ Features

- 🎧 **Music / Audio Mode**: Extracts best audio stream, converts to **MP3** (up to 320 kbps), embeds cover art (album art) and ID3 metadata (artist, title, release year). Also supports M4A, FLAC, and OPUS.
- 📺 **Video Mode**: Downloads high-definition video (up to 4K / 1080p) combining DASH video and audio streams into an optimized **MP4** container.
- 📑 **Playlist Support**: Downloads entire playlists into numbered, organized folders.
- 🖥️ **Interactive Terminal UI**: Run `ytdl` without arguments for an interactive menu with colors and progress bars.
- 🍪 **Cookies Support**: Pass `--cookies <browser>` (Firefox, Chrome, Brave) to seamlessly bypass age restrictions or bot verifications.
- ⚡ **Lightning Fast & Typed**: Managed by `uv`, strict typing, and formatted with Ruff.

---

## 🛠️ Prerequisites

1. **Python 3.14+**
2. **[uv](https://docs.astral.sh/uv/)** (recommended package manager)
3. **FFmpeg** installed on your system (for audio conversion and stream merging):
   ```bash
   # Ubuntu / Debian
   sudo apt install ffmpeg

   # Arch Linux
   sudo pacman -S ffmpeg

   # macOS (Homebrew)
   brew install ffmpeg
   ```

---

## 🚀 Quick Start

Clone or open the repository and install the project with `uv`:

```bash
uv sync
```

---

## 📖 Usage Examples

### 1. Interactive Mode (Easiest)
Simply run without arguments:
```bash
uv run ytdl
```
Follow the interactive prompt to choose video, audio, or playlist, select resolution/bitrate, and paste the URL.

---

### 2. Audio Only (Music & Clips)
Download and convert to 320 kbps MP3 with embedded cover art:
```bash
uv run ytdl audio "https://www.youtube.com/watch?v=VIDEO_ID"
```

Customize bitrate or format:
```bash
# 256 kbps M4A
uv run ytdl audio "https://www.youtube.com/watch?v=VIDEO_ID" --quality 256 --format m4a

# Custom output directory
uv run ytdl audio "https://www.youtube.com/watch?v=VIDEO_ID" -o ~/Music
```

---

### 3. Video Download
Download the best available quality merged into MP4:
```bash
uv run ytdl video "https://www.youtube.com/watch?v=VIDEO_ID"
```

Limit maximum resolution (e.g. 1080p):
```bash
uv run ytdl video "https://www.youtube.com/watch?v=VIDEO_ID" --resolution 1080
```

---

### 4. Playlist Download
Download a full playlist into a dedicated folder:
```bash
# As videos
uv run ytdl playlist "https://www.youtube.com/playlist?list=PLAYLIST_ID"

# As MP3 audio files
uv run ytdl playlist "https://www.youtube.com/playlist?list=PLAYLIST_ID" --audio

# Download only items 1 to 5
uv run ytdl playlist "https://www.youtube.com/playlist?list=PLAYLIST_ID" --items 1-5
```

---

### 5. Age-restricted & Protected Videos (Cookies)
If YouTube requires authentication:
```bash
uv run ytdl video "https://www.youtube.com/watch?v=VIDEO_ID" --cookies firefox
```

---

## 📁 Output Directory

By default, downloads are saved in:
```text
~/Downloads/yt-downloader/
├── audio/
├── video/
└── playlists/
```

You can change the default directory by setting the `YTDL_DOWNLOAD_DIR` environment variable:
```bash
export YTDL_DOWNLOAD_DIR="/path/to/my/downloads"
```

---

## 🧪 Development & Quality Checks

```bash
# Run unit tests
uv run pytest

# Check code formatting & linting
uv run ruff check .
uv run ruff format --check .

# Run type checker
uv run pyright
```

---

## 🤖 AI Assistance & Agents
See [AGENTS.md](AGENTS.md) for architectural guidelines, strict tooling rules, and agent roles when collaborating with AI assistants (Gemini, Antigravity, OpenAI Codex, Claude).
