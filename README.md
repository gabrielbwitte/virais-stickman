# Stickman Explainer Engine — Hermes Skill

Skill Hermes para produzir vídeos explicativos narrados com bonecos palito. Aceita temas pesquisáveis, prepara roteiro e pacote para YouTube, mantém âncoras de personagem e paleta por projeto, gera imagens/clipes usando os provedores configurados no Hermes e renderiza o MP4 localmente com FFmpeg.

## Estrutura

```text
skills/stickman-explainer-engine/
├── SKILL.md
├── references/
└── scripts/
```

## Instalação no Hermes

Depois de publicar este repositório no GitHub, instale a skill diretamente:

```bash
hermes skills inspect <owner>/<repo>/skills/stickman-explainer-engine
hermes skills install <owner>/<repo>/skills/stickman-explainer-engine
```

Ou adicione o repositório como fonte (tap) e instale a skill:

```bash
hermes skills tap add <owner>/<repo>
hermes skills search stickman --source <owner>/<repo>
hermes skills install <owner>/<repo>/stickman-explainer-engine
```

Confirme a instalação e inicie a produção:

```bash
hermes skills list
```

No chat Hermes, use `/stickman-explainer-engine` ou `/stickman-explainer-engine <pedido>`.

## Requisitos

- Hermes Agent com ferramentas `web_search`/`web_extract`, `text_to_speech`, `image_generate` e `write_file` disponíveis.
- Configuração de provedores de imagem e áudio feita por `hermes tools`.
- `video_gen` habilitado em `hermes tools` para gerar clipes; sem ele, a skill pode trabalhar com imagens estáticas.
- `ffmpeg` e `ffprobe` disponíveis no mesmo backend de terminal usado pelo Hermes para produzir o arquivo final local.

Use `hermes config migrate` para preencher a configuração não sensível `stickman.output_dir`; o padrão é `~/.hermes/cache/stickman-outputs`. Credenciais dos provedores devem ser gerenciadas pelo Hermes, nunca gravadas neste repositório.

## Testes locais

Os testes de renderização usam FFmpeg local se ele estiver instalado; caso contrário, essa verificação é ignorada.

```bash
python3 -m unittest discover -s tests -v
```

## Licença e autoria

Este repositório usa a licença [MIT](LICENSE). O conteúdo e scripts da skill podem ser reutilizados conforme os termos dessa licença.
