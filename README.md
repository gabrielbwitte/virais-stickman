# Stickman Explainer Engine — Hermes Skill

Skill para Hermes Agent que produz vídeos explicativos narrados em estilo boneco palito. Aceita temas pesquisáveis, prepara roteiro e pacote para YouTube, mantém âncoras de personagem e paleta por projeto, gera imagens e clipes com os provedores configurados no Hermes e renderiza o MP4 localmente com FFmpeg.

## Estrutura

```text
skills/stickman-explainer-engine/
├── SKILL.md
├── references/
└── scripts/
```

## Instalação

Instale a skill diretamente do GitHub:

```bash
hermes skills inspect gabrielbwitte/virais-stickman/skills/stickman-explainer-engine
hermes skills install gabrielbwitte/virais-stickman/skills/stickman-explainer-engine
```

Confirme que ela está disponível:

```bash
hermes skills list
```

Em uma conversa com o Hermes, inicie a produção com `/stickman-explainer-engine` ou envie um pedido junto ao comando, por exemplo: `/stickman-explainer-engine faça um vídeo sobre vulcões`.

## O que a skill produz

- Ideias, roteiro pesquisado e pacote de publicação para YouTube (título, thumbnail, descrição e tags).
- Paleta e saturação escolhidas por projeto, âncoras de personagem e prompts de cena revisáveis.
- Imagens por cena e, quando a ferramenta de vídeo estiver habilitada, clipes animados.
- Um vídeo MP4 montado localmente com FFmpeg, sincronizado à narração.

## Requisitos e configuração

- Hermes Agent com as ferramentas `web_search`, `web_extract`, `text_to_speech`, `image_generate` e `write_file` habilitadas para os recursos correspondentes.
- Provedores de áudio e imagem configurados no Hermes (`hermes tools`). Os modelos são controlados pela configuração ativa do Hermes.
- `video_gen` habilitado em `hermes tools` para gerar clipes. Sem ele, a skill pode usar imagens estáticas.
- `ffmpeg` e `ffprobe` disponíveis no backend de terminal do Hermes para renderizar o vídeo localmente.

Use `hermes config migrate` para configurar `stickman.output_dir`; o padrão é `~/.hermes/cache/stickman-outputs`. Gerencie as credenciais dos provedores pelo Hermes e nunca as grave neste repositório.

## Testes locais

Os testes de renderização usam FFmpeg local se ele estiver instalado; caso contrário, essa verificação é ignorada.

```bash
python3 -m unittest discover -s tests -v
```

## Licença e autoria

Este projeto está sob a licença [MIT](LICENSE). Consulte o arquivo da licença para os termos de uso, modificação e redistribuição.
