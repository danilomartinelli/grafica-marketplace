---
name: export
description: "Gera os arquivos finais de uma peça impressa já desenhada: PDF vetorial com sangria e marcas de corte, conversão CMYK pelo perfil ICC, imagem no DPI da distância, prévia e ficha técnica pronta para mandar à gráfica. Use quando pedirem os arquivos finais, o PDF, CMYK, outra resolução ou a ficha para a gráfica."
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rasterizar.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/preflight.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_deps.py) Bash(pdftoppm *) Bash(pdftocairo *) Bash(pdfimages *) Bash(pdffonts *) Bash(pdfinfo *)"
license: "MIT (código e textos); fontes empacotadas sob SIL OFL 1.1 — ver LICENSE"
---

# /grafica:export

**Pedido:** $ARGUMENTS
**Uso:** `/grafica:export [peça] [--cmyk] [--dpi N]`

> **RAIZ** = pasta do plugin: `${CLAUDE_PLUGIN_ROOT}`. Se a variável não aparecer resolvida, use a pasta-base informada ao carregar esta skill e suba dois níveis; se você chegou aqui a partir de outra skill do plugin (ex.: craft → grill), use a mesma RAIZ dela. Antes de começar, leia `RAIZ/nucleo/principios.md` (princípios, ferramentas e padrão de entrega) e, uma vez por sessão, rode `python3 RAIZ/scripts/check_deps.py` (se faltar algo ou o Python tiver outro nome, siga `/grafica:setup` — `RAIZ/skills/setup/SKILL.md`).

Gera os arquivos finais e a ficha para a gráfica. Chamado no fim do `craft`, depois de `bolder`/`polish`/`adapt`, ou sozinho.

## Arquivos

1. **PDF para a gráfica** — o PDF do kit já é o final: vetorial, tamanho real, TrimBox/BleedBox, fontes incorporadas.
   - Papel (cartão, flyer, cartaz): gere com `marcas_corte=True` se a gráfica não disser o contrário. Gráficas online costumam pedir **sem marcas e com sangria** — siga o gabarito delas quando houver.
   - Lona, faixa, adesivo grande: sem marcas de corte.
   - Nome: `<marca>-<peca>-<L>x<A>cm.pdf`.
2. **Imagem no DPI da peça** — `python3 RAIZ/scripts/rasterizar.py peca.pdf` (DPI da distância, lido do `.spec.json`).
   - Se o usuário pediu um DPI explícito (ex.: "300 dpi" num banner de 2 m), **faça o que ele pediu** e informe megapixels e MB; ofereça a versão no DPI recomendado se for bem menor.
   - Tem foto → JPEG q92 (PNG com foto em tamanho grande passa de centenas de MB). Só vetor → PNG.
   - Frente e verso: `--pagina 1` e `--pagina 2`.
   - Lado > 8000 px: zipe para entregar no chat (o app não pré-visualiza imagens tão grandes).
3. **Prévia** — `python3 RAIZ/scripts/rasterizar.py peca.pdf --previa` (≈ 1800 px), para mostrar e para mandar no WhatsApp do cliente.
4. **`direcao-de-arte.md`** — o manifesto da peça (passo 4 do craft), para o cliente e para manter a família visual nas próximas peças.
5. **Ficha para a gráfica** (no texto da resposta, pronta para copiar):

```
Peça: Banner — Rodízio do almoço
Tamanho final: 200 × 80 cm (horizontal) · arquivo com 1 cm de sangria em cada lado
Material: lona 440 g, impressão digital 4 cores
Acabamento: ilhós nos 4 cantos e a cada 50 cm · refile
Cores: RGB (converter para CMYK com o perfil da gráfica)
Arquivo: tichao-banner-200x80cm.pdf (fontes incorporadas, fotos a 93 dpi efetivos)
Quantidade: (a confirmar)
```

Ajuste os campos ao tipo (cartão: papel couchê 300 g, laminação fosca/verniz localizado, frente e verso 4×4; flyer: couchê 115/150 g, 4×4 ou 4×0; adesivo: vinil, recorte; placa: PVC 2 mm/ACM).

## Cor (RGB × CMYK)

O kit trabalha em RGB e a maioria das gráficas rápidas e digitais aceita. Para offset ou quando a gráfica exigir CMYK, gere a peça com `Peca(..., cores="cmyk")`:
- Vetores e fotos são convertidos pelo perfil ICC: o da gráfica se você definir `GRAFICA_ICC=/caminho/perfil.icc` (peça a eles), senão o FOGRA39 que existir no sistema. O relatório e o `.spec.json` dizem qual foi usado.
- Fotos com transparência (fades) são achatadas sobre a cor de fundo — passe `compor_sobre=` se o fundo atrás da foto não for a última cor de `fundo()`.
- Logo PNG com transparência fica em RGB (o kit avisa): para CMYK puro, peça o logo vetorial ou desenhe com formas do kit.
- Cores que caem na conversão (verde-limão, azul elétrico, laranja neon, rosa choque) mudam: mostre a prévia do PDF CMYK ao usuário e sugira prova de cor quando a cor da marca for crítica (`RAIZ/references/cor.md`).
- Cores já especificadas em CMYK pela marca podem entrar direto: `cor("cmyk(0,35,85,0)")`.

## Entregar

Envie PDF, imagem (zip se preciso) e prévia, cada um com uma linha de contexto. Depois: a ficha, os placeholders a conferir (se houver) e um próximo passo (geralmente `canva` ou `adapt`).
