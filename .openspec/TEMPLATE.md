# OpenSpec Template — yt-downloader

> **Instruções**: Toda nova funcionalidade relevante, mudança arquitetural ou expansão de escopo do `yt-downloader` deve iniciar com uma especificação baseada neste modelo, salva em `.openspec/active/<nome-da-feature>.md`.

---

# RFC: [Nome Conciso da Funcionalidade]

- **Autor**: [Seu Nome ou Agente IA]
- **Data**: [AAAA-MM-DD]
- **Status**: `draft` <!-- draft | in-review | approved | implemented -->
- **Prioridade**: `medium` <!-- low | medium | high -->
- **Componentes Afetados**: `core`, `cli`, `config`, `models`

---

## 1. Contexto & Motivação
- Qual é o problema ou necessidade que esta mudança resolve?
- Por que a implementação atual é insuficiente?

---

## 2. Escopo
- **Dentro do escopo**:
  - Item 1...
  - Item 2...
- **Fora do escopo (não-objetivos)**:
  - O que deliberadamente NÃO será feito agora?

---

## 3. Contrato da Interface (CLI & UX)
Descreva como o usuário interagirá com a funcionalidade:

```bash
# Exemplo de comando
uv run ytdl [subcomando] <url> --flag valor
```

- **Novos argumentos / flags**:
  - `--flag-exemplo`: Descrição, tipo e valor padrão.
- **Saída visual esperada**: (barras de progresso, mensagens do Rich, tratamento de erro).

---

## 4. Arquitetura Técnica & Decisões de Design
- **Integração com `yt-dlp`**: Quais opções, hooks ou pós-processadores FFmpeg serão necessários?
- **Modelos (`src/yt_downloader/core/models.py`)**: Quais dataclasses ou enums serão criados/modificados?
- **Configuração (`src/yt_downloader/config.py`)**: Alguma nova variável de ambiente ou caminho?

---

## 5. Critérios de Aceite
- [ ] O comando funciona com parâmetros válidos.
- [ ] Trata erros graciosamente com mensagens claras (sem stack traces não capturadas).
- [ ] Respeita o padrão de saída e organização de pastas do projeto.
- [ ] Mantém conformidade com Python 3.14 e tipagem estrita no Pyright.

---

## 6. Plano de Testes & Mocks
- Quais testes unitários serão adicionados em `tests/unit/`?
- Quais métodos do `yt_dlp.YoutubeDL` serão mockados para garantir que não haja requisições à rede?
- Comandos de validação:
  ```bash
  uv run ruff check .
  uv run ruff format --check .
  uv run pyright
  uv run pytest
  ```
