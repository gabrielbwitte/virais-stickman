---
name: stickman-explainer-engine
description: Create narrated stick-figure explainer videos.
version: 0.1.0
author: Gabriel Witte (gabrielbwitte), Hermes Agent
metadata:
  hermes:
    tags: [creative, video-production, storytelling]
    config:
      - key: stickman.output_dir
        description: Directory for generated project files; use a Hermes media-delivery directory.
        default: "~/.hermes/cache/stickman-outputs"
        prompt: Where should this video's files be saved?
---

# Stickman Explainer Engine

Cria vídeos explicativos narrados sobre temas pesquisáveis, com roteiro, elenco, fichas, visuais de cena e pacote para YouTube. O usuário escolhe a paleta e a saturação; imagens e clipes usam ferramentas configuradas no Hermes, e a montagem final é local com FFmpeg quando disponível.

## When to Use

Use quando o usuário quiser criar ou desenvolver um vídeo narrado em estilo boneco palito sobre história, ciência, tecnologia, natureza, cultura, sociedade ou outro tema pesquisável, desde a ideia até roteiro, cenas, thumbnail e metadados.

## Prerequisites

- Use as ferramentas Hermes disponíveis, em especial `web_search`/`web_extract` para pesquisa, `text_to_speech` para áudio, `image_generate` para imagens e `write_file` para salvar prompts; `video_generate` é opcional. Confira as descrições e capacidades reais das ferramentas na sessão.
- `video_generate` pode exigir que o toolset `video_gen` esteja habilitado. Se uma ferramenta não estiver disponível, informe a limitação e não simule sua execução.
- Antes de construir prompts, leia `references/visual-guide.md`, `references/image-prompt-workflow.md` e `references/hermes-media-tools.md` com `read_file`, usando `${HERMES_SKILL_DIR}` para localizar os arquivos.
- Antes de montar a EDL/renderização, leia `references/timeline-format.md`.
- Antes de conceber a embalagem ou escrever o roteiro, leia `references/youtube-storytelling.md`.
- Salve arquivos no diretório `stickman.output_dir` configurado pelo Hermes. Não grave credenciais em arquivos de projeto nem peça segredos em conversas do gateway.

## How to Run

Ao iniciar, apresente as dez ideias do Passo 1 e aguarde. Faça as etapas na ordem. Em pontos de aprovação, ofereça somente duas ações: **Sim** aprova o item atual e continua; **Descreva** recebe mudanças, refaz somente o item atual e pede aprovação novamente. Preserve as aprovações anteriores.

Perguntas que precisam coletar valores concretos — como ideia, proporção ou duração — podem apresentar opções numeradas e aceitar valores personalizados. Não substitua esses valores por Sim/Descreva.

## Quick Reference

| Artefato | Local no projeto |
|---|---|
| Manifesto, mapa e linha de edição | `manifesto_producao.json`, `mapa_cenas.json`, `timeline.json` |
| Metadados YouTube | `youtube_metadata.md` |
| Narração e vídeo final | `narracao.mp3`, `video_final.mp4` |
| Prompts de cena | `cenas/cena_<NNN>_descricao.txt`, `_imagem.txt`, `_video.txt` |
| Imagens/clipes | `cenas/cena_<NNN>.png`, `cena_<NNN>.mp4` |
| Âncoras/fichas | `personagem_<slug>_anchor.png`, `personagem_<slug>_identidade.txt`, `personagem_<slug>_anchor_prompt.txt`, fichas A/B |
| Direção visual | Paleta/saturação no manifesto; `style_anchor.txt` formado pelo núcleo fixo + escolhas aprovadas |

Use nomes estáveis e numeração com zeros. `scripts/init_project.py` inicializa o projeto sem fixar a quantidade/duração de cenas; `scripts/render_video.py` monta imagens/clipes com durações e transições variáveis e áudio usando FFmpeg local.

## Procedure

### Passo 1 — Ideias

Na primeira resposta, ofereça exatamente dez ideias pesquisáveis e variadas, distribuídas entre história, ciência, tecnologia, natureza, cultura e sociedade. Histórias bíblicas podem aparecer como uma categoria, não como limite. Prefira ideias visualmente claras e sustentadas por fontes confiáveis; evite conspirações e fatos inventados. Cada item tem título e uma frase de enfoque. O usuário também pode descrever qualquer tema próprio. Termine com: **“Escolha um número ou descreva o seu próprio.”** Aguarde.

### Passo 2 — Proporção

Após a escolha da ideia, pergunte:

“Qual proporção de tela você deseja?
1. 16:9 — YouTube / Paisagem
2. 9:16 — Shorts, TikTok e Momentos
3. 1:1 — Quadrado
Responda com 1, 2, 3 ou digite sua própria proporção.”

Guarde a proporção para todo o vídeo. A miniatura permanece 16:9. Aguarde.

### Passo 3 — Duração e inicialização

Pergunte a duração em minutos; sugira 1, 2, 3 ou 5 minutos e aceite valores personalizados. Converta para duração-alvo em segundos. Não derive a contagem de cenas de blocos fixos de quatro segundos; o número final virá da segmentação semântica do roteiro e da duração de cada batida.

Crie um slug seguro e inicialize o projeto chamando `python3 "${HERMES_SKILL_DIR}/scripts/init_project.py" --slug <slug> --duration-minutes <minutos> --output-dir <diretório-configurado> --aspect-ratio <proporção>` por `terminal`. O diretório configurado é injetado pelo Hermes; se estiver ausente, use `~/.hermes/cache/stickman-outputs`. O script não pode sobrescrever manifesto existente. Se o projeto já existir, retome a partir do primeiro artefato pendente. Aguarde a duração antes de continuar.

### Passo 3B — Paleta e saturação

Antes de título, roteiro ou geração visual, leia `references/visual-guide.md` e proponha uma combinação apropriada ao tema. As paletas disponíveis são quente/terrosa, fria, neutra, pastel ou personalizada; saturação baixa/mutada, média/natural ou alta/viva porém controlada. A House Style não fixa mais as cores: o desenho 2D, anatomia, contorno, textura e vinheta continuam invariáveis; paleta e saturação são variáveis escolhidas pelo usuário.

Pergunte:

“Quer seguir com esta paleta e saturação para todo o projeto?
1. Sim — aprovar a combinação sugerida: <paleta> + <saturação>.
2. Descreva — diga a paleta e intensidade que prefere (ex.: fria + saturação média).”

Se receber “Descreva”, interprete a preferência em termos visuais concretos, mostre a combinação revisada e pergunte novamente. Persista `palette` e `saturation` no manifesto. Depois, componha `<projeto>/style_anchor.txt` copiando literalmente o STYLE ANCHOR CORE de `references/visual-guide.md` e preenchendo `{PALETTE_DESCRIPTION}` e `{SATURATION_DESCRIPTION}` em inglês com os descritores aprovados. Reuse exatamente esse bloco em âncoras, fichas, cenas, clipes e thumbnail. Aguarde **Sim** antes de continuar. Se a paleta for alterada após gerar imagens, explique que será necessário regenerar as imagens afetadas para evitar misturar estilos.

### Passo 3C — Promessa, título e conceito de thumbnail

Antes de escrever o roteiro, leia `references/youtube-storytelling.md`, defina o público pretendido (por padrão, público geral curioso) e a promessa central do vídeo. Crie uma proposta de título curto e preciso junto com um conceito de thumbnail que desperte curiosidade sem prometer algo que o vídeo não entrega. Use a paleta e a saturação já aprovadas. Pergunte:

“Quer seguir com esta promessa, título e conceito de thumbnail?
1. Sim — usar esta embalagem como guia do roteiro.
2. Descreva — diga o que deseja mudar no público, título ou thumbnail.”

Se receber “Descreva”, refaça apenas a embalagem e peça aprovação novamente. Registre a promessa/título/conceito aprovados. O roteiro deve abrir cumprindo essa promessa, não apenas mencioná-la.

### Passo 4 — Pesquisa e roteiro

Pesquise o tema com `web_search` e `web_extract`, se disponíveis. Separe fatos de interpretações; guarde as fontes consultadas. Se não houver pesquisa disponível, informe a limitação e não invente fatos, datas ou números.

Escreva a narração com 135–150 palavras por minuto (alvo inicial: minutos × 140), em português claro e coloquial. Use estrutura **promessa → progresso → payoff**: comece com uma pergunta, imagem verbal ou consequência intrigante; identifique logo o assunto e a promessa do título; plante uma pergunta central que o vídeo responderá; avance por fatos/reviravoltas com pequenos payoffs e perguntas naturais; encerre resolvendo a pergunta inicial. Evite saudações, introduções genéricas, contexto que possa ser apresentado depois e cliffhangers artificiais. A abertura deve corresponder ao título e à thumbnail, especialmente nos primeiros 30 segundos.

Divida o roteiro em batidas semânticas — cada uma é uma unidade visual que pode ser mostrada numa imagem ou clipe. Não imponha uma quantidade fixa nem duração igual às batidas. Planeje janelas de imagem variáveis conforme texto, ritmo, pausas e importância: como ponto de partida, cenas rápidas podem durar cerca de 2–3,5 s; explicações/revelações, 3–6 s; e um payoff visual ou momento contemplativo pode sustentar mais tempo. São referências, não limites. Una batidas curtas que ficariam ilegíveis e divida trechos longos quando houver mudança visual/narrativa.

Guarde para cada batida o trecho literal, contagem de palavras, intenção, personagens, ação visual, fonte e duração estimada. Após o TTS, ajuste proporcionalmente ao tempo real do áudio, reposicione limites para acompanhar frases, pausas e revelações e salve o plano em `mapa_cenas.json`. A soma das durações de cena deve cobrir exatamente a faixa de narração. Registre separadamente cada transição escolhida na futura `timeline.json`.

Mostre o roteiro como um único bloco contínuo, sem números, legendas, marcações ou texto editorial. Depois pergunte:

“O roteiro está aprovado para gerar a narração?
1. Sim — aprovar e continuar.
2. Descreva — informe o que quer mudar; vou revisar o roteiro e pedir aprovação novamente.”

Se o usuário alterar as palavras, refaça roteiro e mapa, e peça aprovação novamente. Aguarde **Sim**.

Após a aprovação do roteiro, refine o pacote usando somente fatos e ângulos que o roteiro realmente entrega: finalize título, conceito da thumbnail, descrição única e tags relevantes. Na descrição, coloque resumo e uma ou duas expressões-chave naturalmente nas primeiras linhas; mantenha-a clara, específica e dentro do limite atual do YouTube. Tags são complementares e têm impacto limitado: use apenas as relevantes e variantes de grafia genuinamente úteis; não encha a descrição de tags. Salve em `youtube_metadata.md` e pergunte:

“O pacote de título, thumbnail, descrição e tags está aprovado?
1. Sim — continuar para gerar o áudio.
2. Descreva — indique o item e as alterações; vou revisar somente esse pacote.”

Só gere áudio após **Sim**. Se a alteração da embalagem mudar a promessa central, volte ao roteiro e peça nova aprovação.

### Passo 4B — Modelo e geração de áudio

Antes de gerar, confira o provedor/modelo/voz expostos pela configuração ou ferramenta Hermes. Pergunte se quer manter a configuração ativa (**Sim**) ou descrever outra (**Descreva**). Não invente o modelo ativo se a ferramenta não o expuser. O modelo/voz de `text_to_speech` é controlado pela configuração Hermes, não presuma que pode ser trocado por parâmetro de chamada. Se o usuário pedir outro, explique como selecionar em `hermes tools` ou na configuração Hermes; não altere configuração global sem aprovação explícita.

Use `text_to_speech` conforme o schema disponível na sessão. Não faça chamada HTTP direta a um provedor como padrão. Se a ferramenta falhar, preserve o roteiro e pergunte se o usuário quer tentar novamente ou mudar a configuração. Conte as palavras antes do TTS; não crie uma versão de áudio diferente do roteiro aprovado. Verifique a duração real quando a ferramenta ou utilitário disponível permitir; se o ritmo não servir, proponha uma revisão do roteiro em vez de alterar texto silenciosamente.

Guarde o áudio em `narracao.mp3` no diretório do projeto quando o retorno da ferramenta permitir. Use `ffprobe` via `terminal` para registrar a duração real e atualizar manifesto/mapa; a duração da narração passa a ser a fonte de tempo do vídeo. Entregue o caminho absoluto do arquivo na resposta para que o gateway Hermes possa anexá-lo. Não use Bot API, token ou chat ID fixo. Depois pergunte:

“A narração está aprovada para seguir ao elenco?
1. Sim — aprovar e continuar.
2. Descreva — diga o que ajustar; vou revisar apenas a narração atual.”

Se o ajuste mudar o texto, volte à aprovação do Passo 4, atualize as batidas e gere novamente só após aprovação. Se mudar apenas voz/entonação, preserve o texto aprovado.

### Passo 5 — Elenco e fichas

Analise o roteiro e liste personagens principais, secundários e grupos genéricos de figurantes. Para cada personagem nomeado, dê papel, função narrativa e roupa/atributos previstos; harmonize as cores da roupa com a paleta aprovada, mantendo cada personagem distinguível. Não use nomes de pessoas reais nas descrições visuais. Pergunte:

“O elenco está aprovado para gerar as fichas?
1. Sim — aprovar e continuar.
2. Descreva — informe alterações; vou revisar o elenco e perguntar novamente.”

Após **Sim**, leia `references/visual-guide.md` e `references/image-prompt-workflow.md`. Para cada personagem nomeado, derive do elenco aprovado um bloco de identidade em inglês e monte um prompt de âncora usando o `style_anchor.txt` aprovado para este projeto. Salve o bloco em `personagem_<slug>_identidade.txt` e o prompt em `personagem_<slug>_anchor_prompt.txt`. Então gere com `image_generate` uma âncora individual — uma figura de corpo inteiro, pose neutra, roupa completa, fundo simples, sem painel nem texto. Entregue a imagem e pergunte:

“Esta imagem pode ser a referência canônica do personagem?
1. Sim — aprovar e usar nas fichas e cenas.
2. Descreva — diga o que ajustar; vou refazer somente a âncora.”

Só após **Sim**, congele âncora, bloco de identidade e prompt de âncora. Gere duas folhas de estudo a partir da âncora: Ficha A (vistas e expressões) e Ficha B (cinco poses em duas fileiras, 3 + 2). Use apenas referências/parâmetros aceitos pelo schema ativo. Não presuma que todo backend aceita imagens de referência. Se o backend não aceitar a âncora, pare e peça uma alternativa antes de gerar cenas com esse personagem.

O modelo de `image_generate` é definido na configuração Hermes e não é um parâmetro por chamada. A preferência por Qwen só pode ser usada se o backend configurado e a ferramenta Hermes realmente oferecerem esse modelo. Se o usuário quiser trocar, explique que a mudança é feita em `hermes tools`/configuração e aguarde confirmação da nova configuração.

Guarde âncora e fichas no diretório do projeto e entregue os caminhos absolutos para anexação pelo gateway. Pergunte:

“As fichas estão aprovadas para usar como referência nas cenas?
1. Sim — aprovar e continuar.
2. Descreva — indique o personagem e os ajustes; vou refazer somente as fichas afetadas.”

Só use fichas/âncoras após aprovação. A referência primária das cenas é `personagem_<slug>_anchor.png`, não a folha multi-painel. Se o usuário mudar identidade, cabelo ou roupa-base, revise e aprove a âncora e as fichas afetadas. Se mudar apenas uma pose/expressão de estudo, refaça somente a ficha afetada. Atualize os prompts futuros de acordo.

### Passo 6 — Briefing visual, modelo e cenas

**Briefing do projeto:** proponha uma direção visual geral derivada do roteiro e pergunte:

“Quer seguir com esta direção visual?
1. Sim — usar a proposta.
2. Descreva — envie a descrição visual geral do projeto.”

Se receber uma descrição, incorpore-a sem substituir a paleta/saturação já aprovada, o estilo-base, os fatos, a segurança ou as âncoras de personagem; mostre a versão revisada e peça aprovação novamente. Uma alteração global de paleta/saturação exige atualizar `style_anchor.txt`, pedir aprovação e regenerar visuais existentes afetados para não misturar estilos. Registre a descrição aprovada no manifesto.

**Modelo de vídeo:** confira se `video_generate` está disponível e leia sua descrição dinâmica de capacidades. Esse toolset pode estar desativado. O modelo é escolhido na configuração Hermes, não por argumento da chamada. Informe o modelo/provedor somente se estiver visível; pergunte se o usuário quer continuar com a configuração ativa (**Sim**) ou descrever outra (**Descreva**). Para mudar, oriente o uso de `hermes tools`/configuração e aguarde a alteração; não mude silenciosamente uma configuração global. Se não houver ferramenta, pergunte se deseja continuar apenas com imagens ou descrever outra integração.

**Plano de cenas:** por lotes de até dez, apresente em português para cada cena: número, duração variável, trecho literal da narração, personagem(s), expressão, pose/posição, enquadramento, objetos usados ou ausência deles, roupa, cenário, luz e uma ação clara. Use a duração estimada pela batida e o áudio real; não force intervalos de quatro segundos. Cenas curtas devem acompanhar ações/informações rápidas; revele, reação e contemplação podem receber mais tempo. O ritmo deve alternar com intenção, sem acelerar continuamente nem deixar imagens sem função. Cada detalhe visual deve corresponder ao texto narrado. Pergunte:

“As descrições destas cenas estão aprovadas para criar os visuais?
1. Sim — aprovar este lote.
2. Descreva — indique o número da cena e o que devo alterar.”

Em “Descreva”, revise somente as cenas indicadas ou o lote atual. Salve descrições aprovadas em `cenas/cena_<NNN>_descricao.txt`; não avance sem **Sim**.

**Prompts e geração:** leia `references/visual-guide.md`, `references/image-prompt-workflow.md` e `references/hermes-media-tools.md`. Construa cada prompt com invariantes compactos + descrição aprovada da cena. Salve em inglês em `cenas/cena_<NNN>_imagem.txt` e, se vídeo estiver aprovado/disponível, `cenas/cena_<NNN>_video.txt`. Anexe a âncora individual aprovada com o parâmetro de referência suportado e identifique-a como referência de identidade, não de cenário/composição. Não repita o bloco completo do personagem quando a âncora já fixa identidade; mantenha no prompt a regra sem nariz/anatomia palito e os invariantes que precisam de reforço. Não use `execute_code` como substituto para ferramentas de mídia Hermes.

Gere primeiro uma **cena-piloto** representativa (escolha a cena com maior risco de identidade/composição). Mostre o quadro e pergunte:

“A cena-piloto corresponde à descrição, identidade e estilo aprovados?
1. Sim — fixar este padrão e continuar.
2. Descreva — indique exatamente o que falhou; vou corrigir só esse aspecto e testar novamente.”

Só após **Sim**, mantenha âncora, bloco de estilo, modelo/configuração e parâmetros iguais e gere as cenas restantes em lotes de até dez; marque a cena-piloto como concluída para não gerá-la de novo. Guarde imagens como `cenas/cena_<NNN>.png` e clipes como `cenas/cena_<NNN>.mp4` quando houver vídeo; registre as referências e configurações usadas. Se o backend limitar duração do vídeo, use o quadro estático como fallback ou complete/corte o clipe na montagem, sem alegar movimento inexistente. Atualize o manifesto após cada resultado e entregue caminhos absolutos para o gateway Hermes.

Após cada lote, pergunte:

“Este lote de cenas está aprovado?
1. Sim — continuar.
2. Descreva — indique as cenas e os ajustes; vou refazer somente os itens afetados.”

Varie enquadramentos com intenção, use uma ação simples por cena e mantenha elenco, paleta e textura consistentes. Aplique as regras de segurança e de estilo de `references/visual-guide.md`.

**Linha de edição:** leia `references/timeline-format.md` e crie `timeline.json` com uma entrada por batida: fonte (`video` se aprovada e disponível; senão imagem), duração visual, `start`/`end`, trecho narrado e transição para a próxima batida (`cut`, `fade`, `dissolve` ou outra suportada). Comece com corte seco como padrão. Use dissolução/fade somente quando mudança de tempo, lugar ou tom justificar; não aplique o mesmo efeito em todas as transições. Um ponto de partida visual para dissoluções é curto (aprox. 0,25–0,6 s), ajustado à cena; nunca deixe a transição encobrir palavra importante ou payoff. Atualize os tempos para que a linha cubra exatamente a duração do áudio.

### Passo 6E — Render local com FFmpeg

Antes da montagem, confirme `ffmpeg` e `ffprobe` com `terminal`. Se faltarem, não instale sem autorização: explique a dependência e peça ao usuário para instalar/configurar ou continuar com os arquivos separados. Não envie o áudio ou as imagens para um serviço externo para renderizar.

Com o projeto como working directory, execute `python3 "${HERMES_SKILL_DIR}/scripts/render_video.py" --project-dir . --timeline timeline.json --audio narracao.mp3 --output video_final_v001.mp4` via `terminal`. O script normaliza todos os clipes para a mesma resolução, FPS constante, pixel format e timebase, usa o filtro `xfade` para transições com sobreposição e concatenação para cortes secos, mistura a narração e gera MP4 localmente. O áudio embutido nos clipes é removido para evitar falas/música indesejadas; a saída final usa a narração aprovada. As durações da linha são janelas de narrativa; o script contabiliza as sobreposições para que a saída não perca tempo e corresponda à duração da narração. Não substitua uma saída existente sem criar nova versão ou pedir autorização.

Verifique o resultado com `ffprobe`: duração, resolução, proporção, FPS e presença de faixas de vídeo/áudio. Faça uma inspeção de reprodução quando houver ferramenta disponível; se houver arquivo ausente, tela preta, erro de filtro ou duração incorreta, corrija o `timeline.json`/render e repita antes de entregar. Salve os parâmetros e o resultado da validação no manifesto.

### Passo 7 — Miniatura

Pergunte:

“Quer gerar a thumbnail com o conceito já aprovado?
1. Sim — usar o conceito aprovado.
2. Descreva — diga o que deseja mudar no título ou na composição.”

Use o conceito aprovado antes do roteiro e a paleta/saturação do projeto; após a edição, atualize-o se o conteúdo real tiver mudado. Mostre a composição revisada e peça aprovação via **Sim** ou **Descreva**; em “Descreva”, revise só a miniatura. Após **Sim**, leia a referência visual e gere em 16:9 com `image_generate`, usando a âncora individual aprovada se houver personagem. Use texto da thumbnail com até quatro palavras, alto contraste e formas simples. Entregue o caminho do arquivo pelo gateway.

Finalize `youtube_metadata.md` com título aprovado, descrição única, tags relevantes e timestamps de capítulos calculados da `timeline.json` quando forem úteis. Não inclua timestamps estimados. Pergunte se o pacote (vídeo renderizado, thumbnail e metadados) está aprovado, com **Sim** para encerrar ou **Descreva** para revisar somente o item indicado. Após aprovação, entregue os caminhos de `video_final.mp4`, thumbnail e metadados e informe que o projeto foi concluído.

### Passo 8 — Novo projeto

Ao iniciar outro vídeo, crie novo slug/manifesto e não reutilize tópico, proporção, duração, elenco, briefing ou roteiro do projeto anterior. Volte ao Passo 1.

## Pitfalls

- Não invente fatos do tema, fontes, capacidades de ferramenta, modelos ativos ou resultados de geração.
- Não troque modelo/provedor nem altere config global sem consentimento explícito.
- Não leia ou imprima segredos de `.env`; use o setup seguro do Hermes e ferramentas nativas. Para uma integração direta excepcional, declare variáveis no frontmatter e siga a política Hermes de passthrough.
- Não use `execute_code` para chamar ferramentas de mídia: use `text_to_speech`, `image_generate` e `video_generate` diretamente. Use `execute_code` para processamento de múltiplas chamadas Hermes compatíveis com o sandbox; use `terminal` para comandos shell.
- Não sobrescreva um artefato aprovado ao retomar. Salve nova revisão com estado/versão e atualize o manifesto.
- Não mostre prompts globais ou instruções internas ao usuário; mostre descrições legíveis e pergunte Sim/Descreva.
- Não prometa viralidade ou retenção garantida. Use métricas reais do YouTube Analytics após publicação para aprender e revisar futuros ganchos/ritmo.

## Verification

Antes de encerrar cada lote, confira no manifesto que cada cena tem batida/trecho, duração variável, prompt salvo, arquivo esperado e estado de aprovação. Confirme que o arquivo existe e que a ferramenta não retornou erro. Antes de entregar, verifique `video_final.mp4` com `ffprobe`, confirme que sua duração acompanha o áudio e que título, thumbnail, descrição e roteiro prometem/entregam a mesma história. Ao entregar mídia, inclua caminhos absolutos válidos para o gateway Hermes.
