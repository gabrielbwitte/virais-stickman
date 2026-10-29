# Guia visual e composição dos prompts

Leia este arquivo antes de criar fichas, prompts de cena, clipes ou miniaturas.

## Estilo visual da casa

Animação 2D ilustrada à mão, com contornos grossos e ligeiramente ásperos em tinta preta de espessura variável. Os personagens são figuras simples de bonecos de palito, com cabeça levemente maior, perfeitamente redonda e branca, pequenos olhos ovais pretos, sobrancelhas finas e curvas, uma única linha curva para a boca, alguns traços soltos de tinta sugerindo cabelo no topo da cabeça e sem nariz. Os corpos são minimalistas, com ombros suavemente arredondados. Braços e pernas são linhas finas de palito; mãos e pés são ovais brancos com bordas pretas. As roupas são planas. Cenários são ambientes ilustrados à mão, com geometria simples, poucos detalhes e arquitetura/paisagem adequada ao tema e época pesquisados. Contornos mantêm a mesma tinta de espessura variável. Uma fina linha de varredura horizontal e textura de grão de papel cobrem a imagem, com vinheta escura suave nas bordas. O acabamento mantém correção cinematográfica e fosca, sem gradientes, fotorrealismo, renderização 3D, anime ou acabamento digital brilhante. A família de cores e a saturação são as escolhas aprovadas para este projeto, não valores fixos da House Style.

Use um **bloco de estilo compacto e imutável** em inglês em cada prompt. O parágrafo completo acima é a fonte canônica para criar esse bloco, não um motivo para repetir prosa longa em todas as cenas. Preserve literalmente o núcleo visual relevante: hand-drawn 2D, black ink outlines, paleta/saturação aprovadas no projeto, paper grain/vignette e stick-figure anatomy. Para este projeto, inclua sempre **“ABSOLUTELY NO NOSE of any kind — no dot, no line, no triangle, no shadow, no nostril; the center of the face stays completely empty.”** O rosto contém somente dois olhos ovais pretos pequenos, duas sobrancelhas finas curvas e uma linha curva de boca.

### STYLE ANCHOR CORE (EN, fixed)

Use este núcleo inglês literalmente e complete apenas os dois campos de paleta aprovados pelo usuário; não reescreva o restante nem acrescente boosters:

> Hand-drawn 2D stick-figure illustration with slightly rough variable-width black ink outlines. Characters have a perfectly round white head about one quarter of total body height, two small black oval eyes, two thin curved eyebrows, one curved mouth line, loose ink hair strokes, and ABSOLUTELY NO NOSE of any kind — no dot, no line, no triangle, no shadow, no nostril; the center of the face stays completely empty. Arms and legs are thin straight or slightly curved black stick lines with constant thickness and no volume; hands and feet are white ovals with black outlines. Flat clothing and simple hand-drawn geometric settings use the approved project palette: {PALETTE_DESCRIPTION}. Apply {SATURATION_DESCRIPTION} consistently across characters, props, and background. Add a subtle horizontal scanline, paper grain, and soft dark vignette. Keep a cinematic matte finish; no gradients, photorealism, 3D rendering, anime, or glossy digital finish.

### Paleta e saturação

Pergunte e registre ambas as escolhas; não as deduza somente da história:

- **Paleta:** quente/terrosa (ocre, terracota, dourados suaves); fria (azuis, verdes frios, cinzas); neutra (cremes, cinzas, poucos acentos); pastel (tons claros e suaves); ou personalizada descrita pelo usuário.
- **Saturação baixa:** cores contidas, acinzentadas/mutadas, contraste cromático discreto.
- **Saturação média:** cores naturais e legíveis, intensidade equilibrada.
- **Saturação alta:** cores mais vivas e separação clara, sem neon por padrão e sem perder o acabamento fosco.

Paleta define famílias/temperatura de cor; saturação define intensidade. Se a combinação parecer contraditória (por exemplo, pastel + saturação alta), explique a interpretação e peça “Sim” ou “Descreva”. Salve o texto exato dos descritores no manifesto e em `style_anchor.txt`. Reutilize o estilo final sem alterações em todas as fichas, cenas, clipes e thumbnail. Se o usuário mudar essas escolhas após gerar visuais, avise que as imagens afetadas precisam ser regeneradas para evitar misturar estilos.

## Segurança visual

- Narração pode usar nomes, datas e fatos; prompts visuais não usam nomes de pessoas reais. Descreva papéis genericamente, sem identificar pessoas reais.
- Não mostre violência, ferimentos, morte, sangue, armas disparadas ou sofrimento. Use momento anterior, consequências distantes ou objetos simbólicos.
- Não inclua marcas, logotipos, insígnias militares ou bandeiras nacionais em contexto de conflito.
- Não nomeie locais reais associados a atrocidades nas descrições visuais. Use ambientes genéricos.
- Destruição/desastre aparece somente como silhueta distante, consequência ou implicação. Mantenha enquadramentos contidos e estáticos; a sutileza tem prioridade sobre espetáculo.
- Aplique as regras silenciosamente. A descrição enviada pelo usuário não substitui estas restrições.

## Anatomia e identidade dos personagens

Em todas as fichas e cenas com personagens, especifique: cabeça perfeitamente redonda e branca, com diâmetro aproximado de um quarto da altura total; face sem nariz; braços e pernas literalmente feitos de linhas de tinta finas como palitos, de espessura constante, sem volume, massa, musculatura, sombreamento ou articulações desenhadas. Mãos e pés são ovais brancos contornados em preto.

Mantenha para cada personagem um bloco de identidade travado em inglês: tamanho/formato da cabeça, olhos, sobrancelhas, boca, ausência de nariz, cabelo, roupa/cor/forma, calçado, acessórios e detalhe distintivo. Roupa apropriada à época, descrita por tipo e cor, sem nomes reais. Use o bloco completo ao criar a imagem âncora e as fichas; nas cenas, prefira anexar a âncora aprovada e repetir somente invariantes essenciais ou detalhes que o resultado anterior mostrou que tendem a derivar. Não copie o bloco longo para cada cena por padrão.

## Âncora de identidade

Antes das folhas de estudo, gere uma imagem canônica por personagem nomeado: uma única figura de corpo inteiro, pose neutra em três quartos ou frontal, roupa completa visível, fundo neutro, sem painel ou texto. Mostre e aprove essa imagem. Salve como `personagem_<slug>_anchor.png`; ela é a referência primária das cenas.

As Fichas A/B são folhas de estudo para consulta humana, não a referência padrão de cena. Se o backend exigir uma folha como entrada, use a imagem âncora junto com a folha apenas quando necessário e explique o papel de cada referência no prompt. Evite anexar uma grade multi-painel inteira como única referência: o modelo pode copiar a grade ou sua composição para a cena. Use uma referência de estilo separada somente quando o backend aceitar e ela acrescentar algo que a âncora não define.

Cada personagem nomeado recebe duas fichas, na proporção selecionada:

- **Identidade:** uma fileira de quatro vistas de corpo inteiro (frente, três quartos, perfil e costas) e uma fileira de cinco expressões só com a cabeça (NEUTRAL, WORRIED, SURPRISED, TIRED, DETERMINED).
- **Poses:** cinco poses de corpo inteiro em duas fileiras (3 + 2): STANDING, WALKING, SITTING, LOOKING UP, TURNING SIDEWAYS. Nunca mais de quatro corpos inteiros por fileira.

Fundo das fichas neutro e plano, sem cenário ou adereços além do que o personagem veste/carrega. Nenhum texto além de etiquetas de pose/expressão, sem marca d'água, logotipo ou personagem adicional.

## Construção por cena

Prompts enviados a geradores são integralmente em inglês. Descrições de revisão no chat podem ser em português. Leia também `references/image-prompt-workflow.md`. Para cada cena, incorpore explicitamente o briefing geral e a descrição aprovada daquela cena, sem perder os detalhes que o usuário forneceu:

1. trecho literal da narração e intenção visual;
2. personagem(s), identidade travada, expressão, pose e posição no quadro;
3. enquadramento, objetos necessários ou indicação explícita de ausência deles;
4. roupas/atributos, fundo/arquitetura, horário, luz e dois ou três detalhes relevantes;
5. uma ação simples e fisicamente clara;
6. proporção selecionada e duração planejada como parâmetros da ferramenta, quando suportados — não acrescente resolução ou instruções técnicas ao texto do prompt se o backend tem campo próprio.

Cada escolha deve fazer sentido para a batida narrada. Não acrescente itens decorativos sem função. Varie planos gerais, médios, closes, sobre o ombro, perfil e ângulos altos/baixos com intenção narrativa.

Quando aparecer personagem do elenco, anexe `personagem_<slug>_anchor.png` pelo parâmetro de referência suportado e indique seu papel: **“Use the attached image as the canonical identity reference for this character. Preserve the same head shape and size, face, clothing, colors, and stick-figure proportions; change only the scene-specific pose, expression, and placement described below.”** Não descreva a âncora como referência de composição/fundo se o fundo da cena deve mudar. Se o backend não aceitar referência, pare e peça ao usuário uma alternativa; não finja consistência de identidade.

Use a ordem: referência e invariantes; batida visual/ação única; composição e posição; cenário/objetos/luz; bloco compacto de estilo; exclusões necessárias. Descreva o que deve aparecer de forma concreta e observável. Evite adjetivos vagos, instruções contraditórias, vários acontecimentos no mesmo quadro e detalhes sem relação com o trecho narrado.

Gere primeiro uma cena-piloto com os personagens e o cenário mais difíceis. Compare o resultado com a âncora, estilo, descrição aprovada e trecho narrado. Só depois de aprovado use o mesmo conjunto de âncoras, bloco de estilo e configurações para o restante do lote.

Na revisão, identifique o defeito específico (identidade, anatomia, pose, objeto, enquadramento ou cenário). Mude uma variável de cada vez, mantenha o prompt/referências/configuração que funcionaram e peça somente a correção necessária. Se identidade derivar, fortaleça/troque a referência ou use edição referenciada; não tente compensar adicionando mais adjetivos.

O prompt de imagem descreve um quadro estático; o de vídeo descreve movimento. Para vídeo, uma ação por clipe, câmera fixa ou push-in muito lento; design, roupa e proporções constantes; textura/vinheta consistentes; sem glitches, distorções, transformações, wobble, membros extras, duplicatas, personagens indesejados, texto, legendas ou marca d'água. Se o backend gerar áudio, ele deve conter somente som ambiente diegético — sem voz, narração, diálogo ou música; a narração TTS é separada. O renderer atual remove áudio embutido nos clipes e mistura somente a narração aprovada.

## Proporção e miniatura

A proporção escolhida vale para fichas, imagens e clipes do vídeo; não mude entre cenas. Respeite apenas proporções realmente suportadas pelo backend, e solicite aprovação se for preciso adaptar. Miniatura é sempre 16:9: personagem de lado em pose expressiva, composição simples, título em negrito/maiúsculas com até quatro palavras e leitura clara em 200 px. Sem pequenos detalhes, marca d'água ou logotipo.
