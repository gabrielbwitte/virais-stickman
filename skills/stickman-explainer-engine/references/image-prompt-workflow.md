# Engenharia de prompts de imagem para cenas consistentes

Leia antes de escrever ou revisar prompts de fichas, cenas e thumbnails. As práticas abaixo são um ponto de partida; modelos diferentes interpretam prompts e referências de forma diferente.

## Princípios

1. **Trate o prompt como especificação visual.** Declare o objetivo da imagem, sujeito, ação, enquadramento, cenário, detalhes relevantes e restrições. Para cenas complexas, use blocos curtos com rótulos em vez de misturar requisitos incompatíveis num parágrafo confuso.
2. **Separe invariantes de variáveis.** Invariantes: identidade aprovada, anatomia, roupa, paleta, acabamento. Variáveis: batida narrativa, pose, expressão, posição, objetos e ambiente. Mude só as variáveis necessárias para a cena.
3. **Atribua papel a cada referência.** A âncora canônica controla identidade; uma referência de estilo controla somente o acabamento; a descrição da cena controla ação, composição e ambiente. Se houver conflito, mantenha a identidade da âncora e siga a composição aprovada, respeitando as regras de segurança.
4. **Use referências visuais para identidade.** A descrição textual sozinha deixa margem para variação. Anexe a âncora aprovada em cada cena com o personagem, se a ferramenta/backend suportar. A referência não garante identidade perfeita: faça QC e não prometa reprodução exata.
5. **Descreva o visível, não só a intenção.** Transforme “épico”, “emocionante” ou “bonito” em enquadramento, gesto, expressão, contraste, iluminação e objetos observáveis. Uma imagem representa um instante; não empilhe várias ações sucessivas nela.
6. **Não sobrecarregue o prompt.** Preserve os detalhes que alteram a imagem; evite boosters genéricos, adjetivos duplicados, instruções contraditórias e a repetição integral de descrições já representadas pela referência. Mantenha o bloco compacto de estilo constante, mas use a âncora para identidade.
7. **Separe texto de parâmetros.** Proporção, tamanho, seed, qualidade, negative prompt e pesos de referência pertencem a campos da ferramenta quando existentes. Não escreva parâmetros no prompt como se todos os modelos os interpretassem igual.
8. **Itere de forma controlada.** Registre prompt, referências, modelo/configuração, proporção e resultado. Compare a saída com a descrição aprovada. Corrija uma categoria por vez e preserve o que já funcionou. Use edição/referência localizada quando o defeito for numa região ou detalhe já aprovado.

## Ordem de composição

Use esta estrutura como template, não como obrigação de um formato proprietário:

```text
REFERENCE / INVARIANTS: [papel da âncora; identidade, roupa e proporções a preservar]
SCENE BEAT: [instante visual que representa literalmente a batida narrada; uma ação]
SUBJECT: [personagem, expressão, pose, posição no quadro e interação com objeto]
COMPOSITION: [plano, ângulo, escala, direção do olhar, espaço negativo]
SETTING: [fundo, arquitetura/paisagem, horário, luz e poucos detalhes relevantes]
STYLE: [bloco compacto e imutável do estilo aprovado]
CONSTRAINTS: [sem nariz; anatomia palito; sem personagens/textos/objetos extra]
```

O prompt final para o modelo é em inglês. Não inclua os nomes reais usados na narração em descrições visuais. Não invente elementos para preencher espaço.

## Fluxo de geração

1. **Âncora:** escolha/gere uma imagem individual limpa para cada personagem, aprove com o usuário e torne-a imutável. Para esta skill: figura única, corpo inteiro, pose neutra, roupa completa e fundo simples.
2. **Folhas de estudo:** gere as vistas/expressões/poses a partir da âncora. Use folhas para inspeção humana; não use um painel inteiro como referência de cena se uma imagem única da personagem estiver disponível.
3. **Cena-piloto:** selecione a cena com maior risco (personagem + ação + cenário), anexe as referências, produza e faça QC antes de gerar os outros lotes.
4. **Lote:** mantenha modelo/configuração, proporção, bloco de estilo e âncoras aprovadas. Varie apenas a descrição específica da cena.
5. **Correção:** compare saída versus requisito, escolha um defeito prioritário e revise somente a instrução correspondente. Salve prompt e saída versionados; não sobrescreva um artefato aprovado sem autorização.

## Checklist de QC

- A imagem comunica a mesma ideia que o trecho literal da narração?
- Há somente o personagem/quantidade de personagens aprovados?
- O personagem corresponde à âncora: cabeça, rosto sem nariz, cabelo, roupa, cores e proporções?
- Expressão, pose, posição, plano, objetos e cenário coincidem com a descrição aprovada?
- Há itens, ações, texto ou símbolos inventados/indesejados?
- O estilo e a paleta continuam alinhados ao bloco fixo?
- A proporção foi definida pelo parâmetro suportado, e não apenas solicitada no texto?

Se falhar, descreva o desvio concreto e altere somente a parte responsável. Gere novamente ou use edição local se a ferramenta suportar. Se o modelo não respeitar uma restrição importante após tentativas controladas, pare, informe o limite e proponha uma alternativa.

## Diferenças entre modelos

- Prefira o schema e as instruções dinâmicas de `image_generate`; confirme suporte real a referências, múltiplas imagens, edição e negative prompts.
- OpenAI recomenda estrutura clara de sujeito/composição/estilo/restrições, referências com papéis definidos e refinamento de uma alteração por vez.
- Qwen-Image-2.1 documenta condicionamento por múltiplas imagens e disponibiliza reescritores de prompt específicos para geração e edição. Use essa expansão somente se o backend Qwen ativo a oferecer; não aplique um template longo do Qwen a outros modelos por padrão.
- Se um reescritor de prompt específico do modelo estiver ativo, trate sua saída como rascunho: confira se não inventou objetos, ação, texto, roupa ou cenário e se preservou a âncora e as instruções aprovadas antes de enviar ao gerador.

## Fontes

- OpenAI, [Image prompting](https://developers.openai.com/api/docs/guides/image-prompting): estrutura, referência com papéis, âncoras de personagem, preservação e iteração.
- Qwen, [Qwen-Image-2.1 README](https://github.com/QwenLM/Qwen-Image-2.1): geração/edição condicionada por imagens, multi-referência e reescritores especializados.
- Qwen, [prompt rewriter de edição](https://github.com/QwenLM/Qwen-Image-2.1/blob/main/prompt_rewrite/prompts/system_prompt_edit.txt): especificidade visual, papel das referências e resolução de ambiguidades para o fluxo Qwen.
- Google, [Gemini image-generation prompting tips](https://blog.google/products-and-platforms/products/gemini/image-generation-prompting-tips/): sujeito, composição, ação, localização, estilo e limites da consistência.
