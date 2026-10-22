---
name: critique
description: "Avalia o design de uma peça impressa (banner, faixa, flyer, cartão, cartaz…) como quem passa na rua: teste dos 3 segundos, hierarquia, simulação de distância, contraste, daltonismo, marca e chamada para ação, com as 3 correções que mais rendem. Use quando pedirem opinião ou crítica sobre o design de uma peça para imprimir. Para checagem técnica de arquivo use audit; para designs abertos no Canva, as skills do Canva."
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rasterizar.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/preflight.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_deps.py) Bash(pdftoppm *) Bash(pdftocairo *) Bash(pdfimages *) Bash(pdffonts *) Bash(pdfinfo *)"
license: "MIT (código e textos); fontes empacotadas sob SIL OFL 1.1 — ver LICENSE"
---

# /grafica:critique [arquivo]

**Pedido:** $ARGUMENTS
**Uso:** `/grafica:critique [arquivo]`

> **RAIZ** = pasta do plugin: `${CLAUDE_PLUGIN_ROOT}`. Se a variável não aparecer resolvida, use a pasta-base informada ao carregar esta skill e suba dois níveis; se você chegou aqui a partir de outra skill do plugin (ex.: craft → grill), use a mesma RAIZ dela. Antes de começar, leia `RAIZ/nucleo/principios.md` (princípios, ferramentas e padrão de entrega) e, uma vez por sessão, rode `python3 RAIZ/scripts/check_deps.py`.

Avalia o design como quem vai passar na frente da peça. Funciona com peças feitas aqui (PDF + `.spec.json`) ou com arquivos do usuário (PDF, JPG, PNG, link do Canva lido via conector).

## Preparar

1. Descubra a distância de leitura e o tamanho real (do `.spec.json`, do pedido, ou pergunte numa frase). Sem isso a crítica fica no achismo.
2. Gere e **abra**:
   - a prévia: `python3 RAIZ/scripts/rasterizar.py peca.pdf --previa --guias` (imagens do usuário: abra direto);
   - a simulação de distância, para peças vistas a mais de 2 m: `python3 RAIZ/scripts/rasterizar.py peca.pdf --simular <m>` (para JPG/PNG do usuário, reduza a imagem para `largura_cm / (0,0291 × metros)` pixels e amplie de volta para olhar);
   - a folha de acessibilidade de cor: `python3 RAIZ/scripts/rasterizar.py peca.pdf --daltonismo` (para imagens do usuário, aplique as matrizes de `simular_cor` do kit).
3. Se houver `.spec.json`, leia o relatório de textos (maiúscula, distância de impacto, distância legível).

## Avaliar — oito critérios, nesta ordem

Para cada um: ✓ (ok), ! (melhorável) ou ✗ (problema), com a evidência concreta (elemento, medida) — nada genérico.

1. **3 segundos** — Na simulação de distância, dá para dizer o quê/quanto/de quem? Escreva a frase que *de fato* se lê.
2. **Hierarquia** — O olho vai primeiro ao N1? Há dois elementos brigando pelo primeiro lugar? Mais de 3 níveis visíveis de longe?
3. **Legibilidade à distância** — N1 ≥ letra de impacto? Informações essenciais ≥ letra mínima? Fontes finas, script ou condensadas demais nos lugares errados?
4. **Cor, contraste e acessibilidade** — As cores da marca estão sendo usadas (e nos papéis certos)? Texto sobre foto sem tratamento? Pares que vibram ou somem? Razão de contraste das informações-chave (alvo ≥ 7:1 na rua, ≥ 4,5:1 mínimo — meça com `contraste`)? Na folha de daltonismo e no cinza, alguma informação some ou depende só de cor? A cor escolhida conversa com o segmento (psicologia, `RAIZ/references/cor.md`)?
5. **Energia × contexto** — A peça grita onde precisa gritar (rua, varejo) ou está sóbria onde precisa de confiança (saúde, jurídico, cartão)? Minimalismo vazio na rua é ✗.
6. **Marca** — Dá para saber de quem é? Logo/nome legível na distância de decisão, sem competir com a oferta?
7. **Ação** — Fica claro o que fazer (entrar, ligar, chamar no WhatsApp, escanear)? O contato está legível para quem se aproxima?
8. **Produção** — Algo perto das bordas/ilhós/bastão/dobra? Sangria? DPI das fotos? (Para a parte técnica completa, sugira `audit`.)

## Entregar

- Uma linha com a **frase dos 3 segundos** como ela é lida hoje.
- A lista dos 8 critérios (✓/!/✗ + evidência).
- **As 3 correções que mais mudam o resultado**, em ordem, cada uma com o comando que a aplica (`bolder`, `quieter`, `polish`, `photo`, ou ajuste direto).
- Pergunte se quer que você aplique. Se o usuário já pediu "critica e corrige", aplique em seguida e mostre antes/depois lado a lado.

Não reescreva a peça inteira numa crítica; aponte e ofereça.
