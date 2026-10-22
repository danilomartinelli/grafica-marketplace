---
name: polish
description: "Acabamento fino de uma peça impressa feita com o plugin grafica — alinhamento, ritmo, tipografia, pares de números, consistência de cor — sem mudar o conceito nem acrescentar elementos. Use quando pedirem para caprichar, refinar ou dar o toque final no design."
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rasterizar.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/preflight.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_deps.py) Bash(pdftoppm *) Bash(pdftocairo *) Bash(pdfimages *) Bash(pdffonts *) Bash(pdfinfo *)"
license: "MIT (código e textos); fontes empacotadas sob SIL OFL 1.1 — ver LICENSE"
---

# /grafica:polish

**Pedido:** $ARGUMENTS
**Uso:** `/grafica:polish [peça]`

> **RAIZ** = pasta do plugin: `${CLAUDE_PLUGIN_ROOT}`. Se a variável não aparecer resolvida, use a pasta-base informada ao carregar esta skill e suba dois níveis; se você chegou aqui a partir de outra skill do plugin (ex.: craft → grill), use a mesma RAIZ dela. Antes de começar, leia `RAIZ/nucleo/principios.md` (princípios, ferramentas e padrão de entrega) e, uma vez por sessão, rode `python3 RAIZ/scripts/check_deps.py`.

Última passada de acabamento. **Não muda o conceito nem adiciona elementos** — deixa o que existe mais preciso. Se a vontade é desenhar algo novo, pare e pergunte: "como deixar o que já está aqui melhor?"

## Lista de verificação (abra a prévia em tamanho grande e vá item por item)

**Alinhamento**
- Blocos alinhados pela tinta, não pela caixa da fonte (o kit faz; confira peças editadas à mão).
- Eixos: todos os elementos de uma coluna compartilham a mesma margem esquerda ou direita, de verdade (meça no `.spec.json`).
- Topos e bases de blocos vizinhos alinhados ou claramente desalinhados — nunca "quase".

**Ritmo e respiro**
- Espaços entre níveis seguem uma escala (ex.: 1×, 1,5×, 2,5× a menor letra). Respiro maior *entre* grupos do que *dentro* deles.
- Nada encostado em nada: tag ↔ título, preço ↔ "por pessoa", texto ↔ foto.
- Margem de segurança visível como respiro, não só respeitada.

**Tipografia**
- Números grandes (preço, telefone): olhe os pares (7-1, 1-1, R-$). O kit não aplica kerning — corrija com `tracking` ou separando partes.
- Caixa-alta pequena com tracking +5 a +10 % da altura; títulos grandes com tracking menor.
- Separadores consistentes (· ou |, não os dois); travessão × hífen; aspas corretas.
- Acentos, cedilha, til presentes e visíveis (não colidindo com a linha de cima).
- Palavra sozinha na última linha de um parágrafo (viúva): reescreva ou ajuste largura.

**Cor e imagem**
- Mesma cor para a mesma função em toda a peça (preço sempre âmbar, por exemplo).
- Fades suaves, sem degrau visível; foto sem halo duro atrás de texto.
- Nenhum elemento com opacidade que vira "sujeira" na impressão (opacidade < 15 % some; 15–30 % em lona pode parecer mancha).

**Texto**
- Sem erros, sem placeholders, mesma grafia de telefone/@ em todo lugar.
- Corte uma palavra se der: toda palavra a menos ajuda a peça de rua.

## Entregar

Antes/depois lado a lado (duas prévias juntas) e a lista do que mudou em uma linha por item. Reexporte se a peça já tinha sido exportada.
