# Formato da timeline

Leia antes de criar `timeline.json` ou chamar `scripts/render_video.py`.

```json
{
  "aspect_ratio": "16:9",
  "fps": 30,
  "scenes": [
    {
      "number": 1,
      "start": 0.0,
      "end": 3.2,
      "duration_seconds": 3.2,
      "narration_excerpt": "Trecho literal da batida um.",
      "image": "cenas/cena_001.png",
      "video": "cenas/cena_001.mp4",
      "transition_out": {"type": "fade", "duration_seconds": 0.35}
    },
    {
      "number": 2,
      "start": 3.2,
      "end": 7.8,
      "duration_seconds": 4.6,
      "narration_excerpt": "Trecho literal da batida dois.",
      "image": "cenas/cena_002.png",
      "transition_out": {"type": "cut", "duration_seconds": 0}
    }
  ]
}
```

- `duration_seconds` é o intervalo narrativo da batida, sem incluir sobreposição de transição. A soma dos intervalos deve ser igual à duração medida de `narracao.mp3`. `start`/`end` são timestamps acumulados de referência e devem acompanhar essas durações.
- `image` é o fallback obrigatório. Se `video` existir e o arquivo estiver presente, o renderizador usa o clipe; caso contrário usa a imagem. Vídeos curtos demais recebem freeze do último frame; vídeos longos demais são cortados para o intervalo mais a transição de saída.
- `transition_out` descreve a passagem desta cena para a próxima. `cut` não sobrepõe tempo. Outros efeitos usam `duration_seconds`; a transição da última cena é ignorada.
- O renderizador compara a soma das durações com o áudio e aplica uma escala proporcional se houver diferença. Use o relatório de render e corrija a timeline se a escala estiver grande; não dependa dessa correção para criar pausas semanticamente erradas.
- O renderizador normaliza resolução, proporção, FPS, timebase e pixel format. Resolução opcional é `[largura, altura]` e deve respeitar a proporção aprovada.
- Entradas são caminhos relativos ao diretório do projeto; o renderizador rejeita caminhos que escapem dessa pasta. Saída padrão: `video_final.mp4`; ele recusa sobrescrever sem autorização explícita.
