# AGENTS.md — Diretrizes para Agentes de IA

Este documento define a governança, padrões arquiteturais, regras de execução e convenções que **todos os agentes de IA** (Gemini, Antigravity, OpenAI Codex, Claude Code e subagentes) devem seguir estritamente ao trabalhar neste repositório.

---

## 1. Visão Geral do Projeto

O **yt-downloader** é uma ferramenta de linha de comando (CLI) modular em Python para download de conteúdo do YouTube (vídeos em alta definição, playlists completas e extração de áudio de alta fidelidade como MP3 com metadados e capa).

---

## 2. Stack Tecnológica e Ferramentas Obrigatórias

- **Linguagem**: Python `>=3.14`
- **Gerenciador de Pacotes e Ambiente**: `uv` (exclusivo)
- **Build Backend**: `hatchling` (PEP 517 / PEP 621)
- **Motor de Download**: `yt-dlp` (exclusivo para interações com YouTube)
- **Pós-processamento Multimídia**: `ffmpeg` (binário do sistema operacional)
- **Interface CLI**: `typer` + `rich`
- **Linter e Formatador**: `ruff`
- **Verificador de Tipos**: `pyright` (modo estrito)
- **Framework de Testes**: `pytest`

---

## 3. Regras Mandatórias de Execução

1. **Uso Exclusivo do `uv`**:
   - NUNCA execute `pip install`, `poetry` ou manipule o `venv` manualmente.
   - Sincronizar dependências: `uv sync`
   - Adicionar dependência: `uv add <pacote>`
   - Adicionar dependência de desenvolvimento: `uv add --dev <pacote>`
   - Executar comandos e scripts: `uv run <comando>`

2. **Proibição Absoluta de Bibliotecas Depreciadas**:
   - NUNCA use `pytube`, `pytubefix` ou `youtube-dl`. O único backend permitido é `yt-dlp`.

3. **Gerenciamento de Arquivos de Mídia**:
   - NUNCA salve mídias baixadas dentro do diretório de código-fonte (`src/`) ou em pastas rastreadas pelo Git.
   - O destino padrão de downloads deve ser `~/Downloads/yt-downloader/` ou pasta indicada explicitamente pelo usuário.
   - Todo arquivo de mídia deve estar devidamente ignorado no `.gitignore`.

4. **Padrão de Qualidade e Tipagem**:
   - Todo código novo em `src/` deve ter anotações de tipo completas (Type Hints em argumentos e retornos).
   - Nenhuma função deve suprimir erros com `except: pass` silencioso. Sempre capture exceções específicas e registre mensagens informativas.
   - Antes de concluir qualquer tarefa, valide:
     ```bash
     uv run ruff check .
     uv run ruff format --check .
     uv run pytest
     ```

5. **Regra de Testes Unitários**:
   - Testes unitários NUNCA devem fazer requisições reais ao YouTube nem baixar arquivos da internet.
   - Use `unittest.mock` para simular o comportamento de `yt_dlp.YoutubeDL`.

---

## 4. Estrutura Arquitetural (`src/` Layout)

```text
yt-downloader/
├── src/
│   └── yt_downloader/
│       ├── __init__.py           # Versão e exports principais
│       ├── cli.py                # Interface CLI (comandos typer e interface rich)
│       ├── config.py             # Configurações globais, paths e detecção de ffmpeg
│       └── core/
│           ├── __init__.py
│           ├── models.py         # Enums, Dataclasses (DownloadOptions, DownloadResult, etc.)
│           └── downloader.py     # Wrapper de alto nível sobre yt_dlp.YoutubeDL
├── tests/
│   ├── unit/                     # Testes unitários com mocks
│   │   ├── test_config.py
│   │   ├── test_downloader.py
│   │   └── test_cli.py
│   └── conftest.py
├── pyproject.toml                # Definição do projeto PEP 621 com hatchling
├── AGENTS.md                     # Este documento de governança
├── README.md                     # Documentação para o usuário final
└── .gitignore                    # Regras de exclusão do Git
```

---

## 5. Especialidades de Agentes / Subagentes

Quando uma tarefa complexa for dividida entre agentes ou subagentes, respeite as seguintes especialidades:

### 1. Engine Specialist (`core/`)
- Responsável por opções do `yt-dlp`, pós-processadores FFmpeg, hooks de progresso e resolução de streams (DASH, extração de áudio, metadados ID3, capas de álbuns e tratamento de cookies do navegador para vídeos com restrição).

### 2. CLI & UX Specialist (`cli.py`)
- Responsável pela experiência do usuário no terminal: menus interativos, comandos e subcomandos, validação de URLs, cores, spinners e barras de progresso via `rich`.

### 3. QA & Quality Specialist (`tests/`, tooling)
- Responsável pela integridade do código, mocks nos testes automatizados, conformidade com o Ruff e compatibilidade com Python 3.14.

---

## 6. Comandos Rápidos de Verificação

```bash
# Sincronizar ambiente
uv sync

# Testar a CLI localmente
uv run ytdl --help

# Rodar os testes
uv run pytest -v

# Verificar lint e formatação
uv run ruff check .
uv run ruff format --check .
```
