# RFC 002: Redesign da Experiência UX — Menus Interativos (Setas/Números), Banner Rich e Progresso Unificado

- **Autor**: CleberNandi & Antigravity (Gemini)
- **Data**: 2026-09-16
- **Status**: `approved`
- **Prioridade**: `high`
- **Componentes Afetados**: `cli`, `ui`, `core/downloader`, `pyproject.toml`

---

## 1. Contexto & Motivação
A interface interativa atual do `yt-downloader` utiliza prompts textuais básicos (`rich.prompt.Prompt.ask`), exigindo que o usuário digite manualmente os nomes das opções (`video`, `audio`, etc.). 

Além disso:
1. O cabeçalho inicial é simples demais e sem identidade visual.
2. Não há suporte a navegação por setas (↑/↓) nem atalhos numéricos (1, 2, 3...).
3. Durante o download de vídeos DASH (vídeo 1080p+ e áudio separados), a barra de progresso sofre instabilidade visual (reseta, duplica linhas ou salta de trás para frente entre os streams).
4. Cancelamento via `Ctrl+C` ou `Esc` despeja tracebacks desnecessários.

Esta RFC implementa a reformulação completa da experiência de terminal (UX).

---

## 2. Escopo
- **Dentro do escopo**:
  - **Banner Premium no Terminal** (`src/yt_downloader/ui/banner.py`):
    - Cabeçalho em ASCII art com bordas arredondadas e badges das tecnologias (`Python 3.14 • uv • yt-dlp • FFmpeg`).
  - **Menus Interativos com Setas e Números** (`src/yt_downloader/ui/prompts.py`):
    - Uso da biblioteca `InquirerPy` (baseada em `prompt_toolkit`).
    - Navegação com setas direcionais (↑ / ↓), seleção por número direto (1, 2, 3...) e digitação para filtro.
    - Menus para:
      - Tipo de download (`🎵 Áudio / Música`, `🎬 Vídeo HD`, `📑 Playlist`, `🚪 Sair`).
      - Resolução de vídeo (`Melhor Disponível`, `1080p`, `720p`, `480p`).
      - Qualidade de áudio (`320 kbps`, `256 kbps`, `192 kbps`, `128 kbps`, `VBR Best`).
      - Formato de áudio (`mp3`, `m4a`, `flac`, `opus`).
  - **Validação Antecipada de URL**:
    - O prompt de link valida em tempo real se a URL é válida e aponta para o YouTube antes de perguntar qualidade/resolução.
  - **Tratamento Gracioso de Cancelamento**:
    - `Ctrl+C` ou `Esc` em qualquer momento encerra a CLI com mensagem limpa (`Operação cancelada pelo usuário.`), sem tracebacks.
  - **Barra de Progresso Unificada e Estável**:
    - Acompanhamento unificado e progressivo em uma única linha no terminal:
      `[1/2] Baixando Vídeo...` ➔ `[2/2] Baixando Áudio...` ➔ `[FFmpeg] Mesclando...`.
    - Ativação de `transient=True` para limpar linhas residuais ao finalizar.
  - **Isolamento de CI e Automação**:
    - Menus do `InquirerPy` rodam exclusivamente no modo interativo (`ytdl` sem argumentos).
    - Comandos por flags (`ytdl video ...`, `ytdl audio ...`) continuam 100% não-interativos para CI e scripts.

- **Fora do escopo**:
  - Interface gráfica de janelas (GUI / Desktop).
  - TUI completa em tela cheia baseada em Textual.

---

## 3. Contrato da Interface (CLI & UX)

### Banner & Menu Interativo:
```text
╭──────────────────────────────────────────────────────────────────────╮
│   __   _______     ____                        _                 _   │
│   \ \ / /_   _|   |  _ \  _____      ___ __   | | ___   __ _  __| |  │
│    \ V /  | |_____| | | |/ _ \ \ /\ / / '_ \  | |/ _ \ / _` |/ _` |  │
│     | |   | |_____| |_| | (_) \ V  V /| | | | | | (_) | (_| | (_| |  │
│     |_|   |_|     |____/ \___/ \_/\_/ |_| |_| |_|\___/ \__,_|\__,_|  │
│                                                                      │
│   Python 3.14 • uv • yt-dlp • FFmpeg • v0.2.0                        │
╰──────────────────────────────────────────────────────────────────────╯

? O que você deseja baixar? (Use ↑/↓ ou digite o número):
 ❯ 1) 🎵 Áudio / Música (MP3 com tags e capa)
   2) 🎬 Vídeo (MP4 em alta definição)
   3) 📑 Playlist Completa
   4) 🚪 Sair
```

### Progresso Estável:
```text
[1/2] Baixando Vídeo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 78% • 14.2 MB/s • 00:02
```
```text
[2/2] Baixando Áudio ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% • 8.5 MB/s • 00:00
```
```text
[FFmpeg] Mesclando vídeo e áudio em MP4...
```

---

## 4. Arquitetura Técnica & Decisões de Design

1. **Nova Dependência**: `inquirerpy>=0.3.4` adicionada via `uv add inquirerpy`.
2. **Submódulo UI (`src/yt_downloader/ui/`)**:
   - `ui/banner.py`: Renderização do cabeçalho em Rich.
   - `ui/prompts.py`: Abstração de menus e validação de URL com captura de `KeyboardInterrupt`.
3. **Refinamento do Progresso em `cli.py`**:
   - Rastreamento contextual do estágio do download sem recriar tarefas concorrentes.

---

## 5. Critérios de Aceite
- [x] Banner estilizado renderizado no início do modo interativo.
- [x] Navegação por setas (↑/↓) e atalhos numéricos (1, 2, 3...) funcionando em todos os prompts.
- [x] URL validada antes de exibir opções de qualidade.
- [x] Cancelamento com `Ctrl+C` ou `Esc` sai de forma limpa.
- [x] Download DASH exibe apenas uma barra de progresso estável e sequencial.
- [x] Comandos diretos continuam não-interativos e cobrem 100% dos testes unitários.
- [x] Formatação com Ruff e tipagem estrita com Pyright sem erros.

---

## 6. Adendo de Refinamentos & Resiliência Pós-Validação

Após validação prática em ambiente real, foram incorporadas as seguintes melhorias evolutivas:

### 1. Migração para `InquirerPy.fuzzy` (Navegação Tripla)
- **Motivação**: O prompt `select` original bloqueava a digitação livre de números (`1`, `2`, `3`) e palavras-chave.
- **Implementação**: Adoção de `inquirer.fuzzy` em todas as seleções interativas, permitindo três métodos combinados:
  - Navegação direcional por setas (`↑`/`↓`).
  - Digitação direta de números de atalho.
  - Filtro preditivo em tempo real por palavras (`video`, `audio`, `320`, `mp3`).

### 2. Tratamento Gracioso de Opções Inválidas com Pausa e Limpeza
- **Motivação**: Entradas sem correspondência retornavam `None`, disparando `sys.exit(0)` involuntário.
- **Implementação**: Em `_safe_execute`:
  - Captura retornos vazios sem encerrar o processo.
  - Exibe alerta estilizado em vermelho e amarelo.
  - Pausa aguardando interação do usuário (`Pressione Enter para voltar ao menu...`).
  - Limpa a tela via `console.clear()` e re-renderiza o cabeçalho (`render_banner(console)`) antes de reexibir o menu sem poluição residual.

### 3. Higienização de Logs e Supressão de Ticks de Progresso
- **Motivação**: Notificações por fragmento de streaming inundavam o arquivo `logs/ytdl.log` com até 19.000 linhas repetitivas e códigos de escape ANSI por download.
- **Implementação**: 
  - Expressão regular stripping ANSI de todas as mensagens.
  - Filtro em `YTDLLogger` descartando ticks intermediários de fragmentos e ETAs transitórios, preservando exclusivamente marcos significativos de rastreabilidade (extração de streams, resoluções, download/conversão de capa, mesclagem FFmpeg e sucesso).

### 4. Tipografia 3D Shadow e Alinhamento Preciso de Bordas
- **Motivação**: Fundo preenchido escuro gerava dentes/recortes no terminal devido a diferenças de contagem de largura de glifos unicode (`⚡` de 2 colunas no Rich vs 1 coluna na fonte do terminal).
- **Implementação**:
  - Remoção de fundo escuro para transparência nativa do terminal.
  - Substituição por marcador neutro `●` (1 célula mono universal).
  - Padronização matemática das linhas da logo 3D Shadow para exatamente 62 colunas com centralização dinâmica do subtítulo.

