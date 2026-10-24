---
name: bolder
description: "Deixa uma peça impressa mais chamativa (formato push): oferta maior, foto protagonista, contraste, selo, peso tipográfico, menos texto — sem perder legibilidade nem a marca. Use quando disserem que ficou fraco, minimalista, sem destaque ou que não chama atenção."
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rasterizar.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/preflight.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_deps.py) Bash(pdftoppm *) Bash(pdftocairo *) Bash(pdfimages *) Bash(pdffonts *) Bash(pdfinfo *)"
license: "MIT (código e textos); fontes empacotadas sob SIL OFL 1.1 — ver LICENSE"
---

# /grafica:bolder

**Pedido:** $ARGUMENTS
**Uso:** `/grafica:bolder [peça]`

> **RAIZ** = pasta do plugin: `${CLAUDE_PLUGIN_ROOT}`. Se a variável não aparecer resolvida, use a pasta-base informada ao carregar esta skill e suba dois níveis; se você chegou aqui a partir de outra skill do plugin (ex.: craft → grill), use a mesma RAIZ dela. Antes de começar, leia `RAIZ/nucleo/principios.md` (princípios, ferramentas e padrão de entrega) e, uma vez por sessão, rode `python3 RAIZ/scripts/check_deps.py` (se faltar algo ou o Python tiver outro nome, siga `/grafica:setup` — `RAIZ/skills/setup/SKILL.md`).

Deixa a peça mais chamativa sem perder legibilidade nem a marca. É a resposta para "ficou fraco", "muito minimalista", "não chama atenção", "não parece propaganda".

## Diagnóstico rápido (1 minuto)

Gere a simulação de distância (`python3 RAIZ/scripts/rasterizar.py --simular <m>`) e responda: o que se vê primeiro? quanto da área o N1 ocupa? há foto? qual o contraste fundo × N1? quanto espaço está "vazio sem função"?

## Alavancas, na ordem em que costumam render mais

1. **N1 maior.** Oferta/preço/palavra-chave ocupando 30–50 % da altura em peças de rua. Use `preco(..., largura_max=..., altura_max=...)` / `cap_para_largura` para chegar ao limite do bloco.
2. **Foto protagonista.** Produto, prato, serviço em close, com opacidade 0,8–1,0, recorte fechado (`zoom`), fade só onde precisa abrir espaço para texto. Ver `/grafica:photo` (`RAIZ/skills/photo/SKILL.md`).
3. **Contraste de fundo.** Fundo chapado escuro com texto claro e um destaque quente (âmbar, amarelo, vermelho) é o padrão mais legível da rua. Fundo claro pede N1 em cor saturada e pesada.
4. **Selo / etiqueta sólida.** Retângulo ou faixa de cor chapada com a palavra-gatilho: PROMOÇÃO, OFERTA, -30 %, NOVO, SÓ HOJE. Uma por peça.
5. **Peso tipográfico.** Trocar para display condensada pesada (Anton, Bebas Neue, Big Shoulders Bold, Archivo Black) no N1/N2. Nunca light/thin à distância.
6. **Cortar texto.** Cada linha secundária removida aumenta o que sobra. Mova detalhes para o verso, para o flyer, ou para "chame no WhatsApp".
7. **Direção e movimento.** Faixa diagonal, foto sangrando na borda, elemento cortado pela margem (de propósito) — use um só recurso.
8. **Cor de destaque única.** Uma cor quente reservada só para preço/CTA; todo o resto em neutros. Mais cores ≠ mais chamativo.

Aplique 2–4 alavancas, não todas. Reavalie com a simulação a cada rodada.

## Limites (o que vira "poluído" ou "brega")

- Explosões/estrelas de clip-art, sombras pretas duras, contorno grosso em tudo, WordArt, gradiente arco-íris.
- Mais de uma etiqueta; mais de 3 cores fortes; tudo em negrito.
- Letra que fica gigante mas condensada a ponto de virar barras de longe (confira na simulação).
- Sacrificar a marca: o nome ainda precisa ser lido na distância de decisão.

## Entregar

Antes/depois lado a lado + as alavancas usadas (1 linha cada). Pergunte se quer ir mais longe ou voltar um passo. Reexporte os arquivos.
