# Ferramentas de mídia e entrega no Hermes

Leia antes de gerar áudio, imagens, clipes ou enviar arquivos.

## Seleção de provedor e modelo

- `text_to_speech`, `image_generate` e `video_generate` usam os provedores/modelos configurados no Hermes. Confira o schema/descrição da ferramenta ativa; não invente modelo ativo nem envie um argumento `model` que a ferramenta não declara.
- Imagem é configurada pelo usuário em **`hermes tools` → Image Generation**. O `image_generate` não oferece troca arbitrária de modelo por chamada. A preferência Qwen só pode ser atendida se o backend e modelo aparecerem na configuração real do Hermes.
- TTS e voz dependem do provedor e da configuração Hermes. `eleven_v3`/`eleven_multilingual_v2` só devem ser oferecidos como opções se o provedor configurado realmente permitir esses IDs. Não troque silenciosamente em caso de erro.
- Vídeo usa o toolset opcional `video_gen`. Quando `video_generate` estiver disponível, leia sua descrição dinâmica: ela informa modalidades e capacidades reais do backend. Backend/modelo são configurados no Hermes; o tool não tem parâmetro de modelo por chamada. Mudanças podem afetar outros usos do usuário e exigem autorização.
- Se o usuário escolher outro modelo, explique a configuração necessária pelo Hermes e aguarde a mudança antes de gerar. Não altere configuração global ou instale provedor sem consentimento explícito.

## Chamadas nativas

- Use `text_to_speech` para áudio, seguindo o schema ativo para texto, voz, velocidade e formato. Guarde o caminho retornado e não altere o roteiro aprovado.
- Use `image_generate` para imagens. Passe `reference_image_urls` ou `image_url` somente quando esses parâmetros existirem no schema e forem aceitos pelo modelo ativo. A ferramenta pode retornar URL ou caminho local.
- Use `video_generate` para texto-para-vídeo ou imagem-para-vídeo quando a ferramenta estiver ativa. `image_url`, `reference_image_urls`, `duration`, `aspect_ratio`, `resolution` e áudio podem ser ignorados/clampados conforme backend; consulte as capacidades da sessão e valide o resultado.
- Não replique endpoints, corpos HTTP ou parâmetros específicos de um provedor dentro da skill como se fossem universais. Use API direta somente quando uma capacidade essencial não estiver disponível na ferramenta Hermes, com autorização do usuário e instruções atuais do provedor.

## Segredos e execução

- Nunca peça ou imprima tokens/chaves no chat; nunca codifique segredos no skill, prompts, manifestos ou scripts.
- Hermes remove variáveis secretas do ambiente de `execute_code` e `terminal` por padrão. Se uma integração HTTP direta for indispensável, declare seus nomes em `required_environment_variables` no frontmatter e respeite o passthrough Hermes. Não presuma que `/opt/data/.env` existe ou está montado.
- Use `execute_code` para workflows com várias chamadas Hermes compatíveis e lógica entre elas. O sandbox expõe somente um subconjunto de ferramentas; não presuma que inclui ferramentas de mídia nem tente chamá-las via `hermes_tools`. Use `terminal` para comandos de shell e ferramentas de mídia diretamente pelo agente.

## Arquivos e entrega

- Use o diretório `stickman.output_dir` configurado no frontmatter. Caminhos absolutos dentro de `~/.hermes/cache/` são preferíveis para entrega nativa; caminhos externos precisam ser permitidos pela política de entrega do ambiente.
- O gateway Hermes pode anexar arquivos de mídia quando a resposta contém o caminho absoluto válido. Para arquivos grandes/de alta resolução, use `[[as_document]]` se o canal aceitar e se for importante preservar os bytes originais; sem isso, Telegram pode recomprimir imagens enviadas como foto.
- Não use Bot API, token ou `chat_id` fixo para entregar mídia em uma sessão gateway. Responda no chat de origem com os caminhos dos arquivos e deixe o Hermes fazer a entrega.
- Se uma ferramenta retornar URL em vez de arquivo local, não invente um caminho: use o método de download disponível/permitido, valide que o arquivo foi salvo no diretório do projeto e então entregue seu caminho.

## Render local com FFmpeg

- Renderize no host local com `ffmpeg` por `terminal`; confirme `ffmpeg` e `ffprobe` no `PATH` antes de começar. Não use renderização externa nem instale pacotes sem autorização.
- Para usar `xfade`, todas as entradas precisam ter a mesma resolução, pixel format, frame rate constante e timebase. `scripts/render_video.py` normaliza esses parâmetros antes de transições.
- Cada cena tem duração-base variável ligada à batida. Uma transição `xfade` sobrepõe imagens e reduz a duração bruta da sequência; o renderer acrescenta esse tempo às entradas e calcula os offsets para conservar o tempo planejado. O áudio TTS é faixa contínua e determina a duração final.
- `render_video.py` remove faixas de áudio embutidas nos clipes gerados e mistura apenas a narração aprovada, evitando fala/música acidental do gerador. Não prometa som ambiente no render final; isso exigiria uma faixa de ambiência aprovada e uma configuração de mix separada.
- Use corte seco para a maioria das trocas. A timeline escolhe explicitamente os fades/dissolves que forem narrativamente necessários. O renderer limita dissoluções muito longas em relação às cenas adjacentes.
- FFmpeg de referência: [filtros `xfade`](https://ffmpeg.org/ffmpeg-filters.html#xfade) e [opções principais](https://ffmpeg.org/ffmpeg-all.html). Verifique o arquivo final com `ffprobe`; não considere um código de saída zero, sozinho, prova de que o render está sincronizado.
