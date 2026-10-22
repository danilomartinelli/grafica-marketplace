---
name: adapt
description: "Adapta uma peça impressa feita com o plugin grafica para outro formato reorganizando a hierarquia (banner → flyer → cartão → cartaz → wind banner → post/story), recalculando distância, letra e DPI. Use quando pedirem a mesma peça em outro tamanho, suporte ou versão digital. Para redimensionar um design que está no Canva, use as skills do Canva."
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rasterizar.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/preflight.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_deps.py) Bash(pdftoppm *) Bash(pdftocairo *) Bash(pdfimages *) Bash(pdffonts *) Bash(pdfinfo *)"
license: "MIT (código e textos); fontes empacotadas sob SIL OFL 1.1 — ver LICENSE"
---

# /grafica:adapt <formato>

**Pedido:** $ARGUMENTS
**Uso:** `/grafica:adapt <formato> [peça]`

> **RAIZ** = pasta do plugin: `${CLAUDE_PLUGIN_ROOT}`. Se a variável não aparecer resolvida, use a pasta-base informada ao carregar esta skill e suba dois níveis; se você chegou aqui a partir de outra skill do plugin (ex.: craft → grill), use a mesma RAIZ dela. Antes de começar, leia `RAIZ/nucleo/principios.md` (princípios, ferramentas e padrão de entrega) e, uma vez por sessão, rode `python3 RAIZ/scripts/check_deps.py`.

Transforma uma peça existente em outro formato — mantendo a identidade, **reorganizando** a hierarquia. Escalar proporcionalmente quase nunca funciona: muda a distância, muda o que cabe, muda o que importa.

## Passos

1. Leia a peça de origem: script `build_*.py`, `.spec.json` e prévia. Extraia: mensagem dos 3 segundos, N1/N2/N3, paleta, fontes, foto, contatos.
2. **Grill** (a skill `/grafica:grill` (`RAIZ/skills/grill/SKILL.md`)), focado no que muda com o formato: onde a nova peça vai ficar (distância), tamanho/material do destino (`RAIZ/references/formatos.md`), o que entra ou sai de conteúdo, e se a mensagem dos 3 segundos continua a mesma. O resto vem da peça de origem.
3. Recalcule letra mínima/impacto e DPI para a nova distância.
4. Reorganize o conteúdo pelo que muda com a distância:

| Origem → Destino | O que muda |
|---|---|
| Banner/faixa (longe) → Flyer (mão) | Entram detalhes: endereço, mapa ou referência, cardápio/serviços, condições, QR. O N1 continua, menor. Frente = chamada; verso = informação. |
| Flyer → Cartaz (1–3 m) | Corta detalhes, aumenta N1, foto maior. |
| Qualquer → Cartão de visita | Só marca + pessoa + contato (+ QR). Nada de oferta datada. |
| Horizontal → Vertical (wind banner, roll-up, story) | Empilha: marca no topo, foto no meio, oferta e CTA embaixo; respeite áreas mortas do suporte (base do roll-up, haste do wind banner). |
| Impresso → Digital (post 1080×1350, story 1080×1920, capa) | RGB, pixels, sem sangria. Truque: 1 cm = 100 px — monte `Peca("post.pdf", 10.8, 13.5, sangria=0, seguranca=0.6, distancia_m=0.4)` e rode `python3 RAIZ/scripts/rasterizar.py post.pdf --dpi 254 --formato png` → 1080×1350 px exatos. Textos-chave ≥ ~3 % da altura (celular); CTA vira "link na bio" / "chame no WhatsApp". |

5. Construa com um novo `build_<peca>-<formato>.py` (copie o de origem e refaça o layout — não só os números). Rode com `PYTHONPATH=RAIZ/scripts python3 build_<peca>-<formato>.py`.
6. Checar, olhar, exportar como no `craft`.

## Entregar

Os arquivos do novo formato + uma prévia lado a lado (origem e destino) para mostrar a família visual. Se pediram vários formatos, entregue todos juntos com a mesma nomenclatura (`<marca>-<peca>-<formato>`).
