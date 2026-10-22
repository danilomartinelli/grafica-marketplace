---
name: quieter
description: "Deixa uma peça impressa mais sóbria e elegante — menos cores, mais respiro, tipografia com contraste de estilo, foto mais calma — mantendo a leitura na distância. Use quando disserem que está gritando demais ou o contexto pede seriedade (saúde, jurídico, convite, cartão)."
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/*) Bash(pdftoppm *) Bash(pdftocairo *) Bash(pdfimages *) Bash(pdffonts *) Bash(pdfinfo *)"
license: "MIT (código e textos); fontes em RAIZ/assets/fonts sob SIL OFL 1.1"
---

# /grafica:quieter

**Pedido:** $ARGUMENTS
**Uso:** `/grafica:quieter [peça]`

> **RAIZ** = pasta do plugin: `${CLAUDE_PLUGIN_ROOT}`. Se a variável não aparecer resolvida, use a pasta-base informada ao carregar esta skill e suba dois níveis; se você chegou aqui a partir de outra skill do plugin (ex.: craft → grill), use a mesma RAIZ dela. Antes de começar, leia `RAIZ/nucleo/principios.md` (princípios, ferramentas e padrão de entrega) e, uma vez por sessão, rode `python3 RAIZ/scripts/check_deps.py`.

Deixa a peça mais sóbria, elegante, confiável — para quando está "gritando demais", "parece panfleto de liquidação", ou o contexto pede seriedade (saúde, advocacia, arquitetura, joalheria, eventos formais).

## Alavancas

1. **Menos cores.** Uma cor de marca + neutros (creme, grafite, off-white). Tire saturação dos destaques ou troque por um tom terroso/metálico (ouro fosco, verde-garrafa, vinho).
2. **Tipografia com contraste de estilo, não de peso.** Serifa de display (Gloock, Young Serif, Instrument Serif) para o nome; sans regular com tracking aberto (Work Sans, Instrument Sans, Montserrat) para o apoio. Pesos médios.
3. **Respiro.** Aumente margens internas e espaços entre grupos; deixe área livre trabalhar como moldura.
4. **Foto mais calma.** Menos opacidade (0,4–0,7), fade mais longo, tons dessaturados ou em duotone com a cor da marca — ou sem foto.
5. **Remover ornamentos.** Selos, faixas diagonais, contornos e sombras saem. Um fio fino ou um detalhe dourado basta.
6. **Alinhamento rigoroso.** Eixo central ou coluna à esquerda, tudo na grade.

## Não exagere

Sóbrio ≠ ilegível. Mesmo numa peça elegante, as informações-chave continuam ≥ letra mínima da distância, e o N1 de uma peça de parede ainda precisa ser lido de onde a pessoa passa. Se a simulação de distância perder a mensagem, recue.

## Entregar

Antes/depois lado a lado + mudanças em uma linha cada. Reexporte.
