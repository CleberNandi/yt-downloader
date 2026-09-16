# RFC 001: Sistema de Observabilidade (Logs) e Resiliência em Falhas de Pós-processamento

- **Autor**: CleberNandi & Antigravity (Gemini)
- **Data**: 2026-09-16
- **Status**: `approved`
- **Prioridade**: `high`
- **Componentes Afetados**: `core`, `cli`, `config`, `models`, `logger`

---

## 1. Contexto & Motivação
Durante um download real de vídeo de alta resolução (1.2 GB), o fluxo de download e a fusão de áudio/vídeo via FFmpeg foram concluídos com 100% de sucesso. No entanto, uma falha na manipulação da thumbnail durante o pós-processamento estourou uma exceção, fazendo a CLI exibir `✗ Download failed!`, embora o arquivo `.mp4` estivesse pronto no disco.

Além disso, o downloader utilizava `quiet: True` e não possuía sistema de logs, impossibilitando diagnosticar erros sem inspecionar o código-fonte ou alterar scripts manualmente.

---

## 2. Escopo
- **Dentro do escopo**:
  - Criação de um módulo central de logging (`src/yt_downloader/logger.py`) com arquivo rotativo (`logs/ytdl.log`) na raiz do repositório.
  - Logger customizado (`YTDLLogger`) para capturar saídas, avisos e erros do motor `yt-dlp`.
  - Suporte à flag global `--verbose` / `-v` em todos os comandos da CLI (`audio`, `video`, `playlist`, `interactive`).
  - Atualização de `DownloadResult` com campo `warnings: list[str]` para suportar **degradação graciosa** (se a mídia principal foi gravada com sucesso mas o pós-processamento de capa/metadado falhou, o status é sucesso com aviso).
  - Feedback visual no Rich informando sobre avisos e apontando para `logs/ytdl.log`.
  - Testes unitários para logging e para degradação graciosa.

- **Fora do escopo (não-objetivos)**:
  - Envio de telemetria ou logs para serviços remotos em nuvem (Sentry, Datadog).
  - Configuração de níveis dinâmicos de log além de INFO/DEBUG via arquivo de configuração externo.

---

## 3. Contrato da Interface (CLI & UX)

### Flags
```bash
uv run ytdl video <URL> --verbose
uv run ytdl audio <URL> -v
uv run ytdl playlist <URL> -v
```

### Comportamento Visual
1. **Download 100% perfeito**:
   - Painel verde com título, arquivo e destino.
2. **Download com falha parcial (ex: capa falhou, mídia salva)**:
   - Painel amarelo com: `✓ Download concluído com avisos!`
   - Exibe o aviso detalhado e indica a consulta a `logs/ytdl.log`.
3. **Download com falha crítica (ex: URL inexistente, erro de rede)**:
   - Painel vermelho com mensagem de erro e indicação para verificar `logs/ytdl.log`.

---

## 4. Arquitetura Técnica & Decisões de Design

### 1. Módulo `src/yt_downloader/logger.py`
- Diretório de log padrão: `Path.cwd() / "logs" / "ytdl.log"`.
- `RotatingFileHandler` com tamanho máximo de 5MB e até 3 backups.
- Função `setup_logging(verbose: bool = False) -> logging.Logger`.
- Classe `YTDLLogger` com métodos `debug()`, `info()`, `warning()`, `error()`.

### 2. Modelo `DownloadResult` em `core/models.py`
```python
@dataclass
class DownloadResult:
    success: bool
    title: str | None = None
    file_paths: list[Path] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    error_message: str | None = None
```

### 3. Tolerância a Falhas em `Downloader.download()`
- Se `extract_info()` disparar exceção, mas arquivos de mídia já existirem em disco no diretório de destino:
  - Verificar se o arquivo principal existe e tem tamanho > 0.
  - Se existir, considerar `success = True`, adicionar o erro da exceção em `warnings` e logar como `warning`.
  - Se não existir, considerar `success = False` com `error_message`.

---

## 5. Critérios de Aceite
- [x] Diretório `logs/` criado automaticamente na raiz do projeto e devidamente ignorado no `.gitignore`.
- [x] Todo comando grava eventos com timestamp em `logs/ytdl.log`.
- [x] A flag `--verbose` / `-v` exibe logs em nível DEBUG no terminal.
- [x] Falhas secundárias de thumbnail/metadados não invalidam arquivos de mídia baixados com sucesso.
- [x] 100% dos testes unitários passam e cobrem o novo comportamento.
- [x] Conformidade total com Ruff e Pyright (modo estrito).

---

## 6. Plano de Testes & Mocks
- `tests/unit/test_logger.py`:
  - Testar criação do arquivo de log e rotação.
  - Testar formatação de mensagens do `YTDLLogger`.
- `tests/unit/test_downloader.py`:
  - Testar cenário de degradação graciosa (exceção durante pós-processamento quando o arquivo de vídeo já existe em disco).
- `tests/unit/test_cli.py`:
  - Testar passagem da flag `--verbose` / `-v`.
