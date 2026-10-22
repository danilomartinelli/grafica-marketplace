---
name: canva
description: "Sobe uma peça impressa feita com o plugin grafica para o Canva do usuário como design no tamanho real (imagem em alta resolução), com aprovação antes de salvar. Use quando pedirem para subir, levar ou salvar no Canva uma peça feita aqui."
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/*) Bash(pdftoppm *) Bash(pdftocairo *) Bash(pdfimages *) Bash(pdffonts *) Bash(pdfinfo *)"
license: "MIT (código e textos); fontes em RAIZ/assets/fonts sob SIL OFL 1.1"
---

# /grafica:canva

**Pedido:** $ARGUMENTS
**Uso:** `/grafica:canva [peça]`

> **RAIZ** = pasta do plugin: `${CLAUDE_PLUGIN_ROOT}`. Se a variável não aparecer resolvida, use a pasta-base informada ao carregar esta skill e suba dois níveis; se você chegou aqui a partir de outra skill do plugin (ex.: craft → grill), use a mesma RAIZ dela. Antes de começar, leia `RAIZ/nucleo/principios.md` (princípios, ferramentas e padrão de entrega) e, uma vez por sessão, rode `python3 RAIZ/scripts/check_deps.py`.

Sobe a peça para o Canva do usuário como um design no tamanho certo. Requer o conector do Canva (ferramentas `mcp__Canva__*`, carregadas por busca de ferramentas). Sem conector: diga que precisa conectá-lo e entregue os arquivos para upload manual.

## O que esperar (diga ao usuário antes, numa frase)

- A peça entra no Canva como **uma imagem em alta resolução** num design do tamanho real. Textos não ficam editáveis lá.
- Subir o PDF pelo conector só guarda o arquivo — **não vira design editável**. Texto editável no Canva exige importar o PDF pela API do Canva (CLI com login do usuário) ou pelo próprio app do Canva; ofereça só se ele quiser.

## Passos

1. **Imagem para o Canva** — `python3 RAIZ/scripts/rasterizar.py peca.pdf --canva`: JPEG ≤ 100 megapixels e ≤ 25 MB (limites de upload do Canva), no maior DPI que cabe.
2. **Tamanho do design** — o Canva mede em px a 96 por polegada: `px = cm ÷ 2,54 × 96` (200 × 80 cm → 7559 × 3024 px). Cada lado vai até 8000 px. Peça maior (ex.: faixa de 300 cm): monte o design em escala (50 %, 25 %) e diga isso — a gráfica deve imprimir pelo PDF, não pelo Canva.
3. **Upload** — `create-upload-url`, depois envie os bytes:
   ```bash
   curl -sS -X POST -H "Content-Type: application/octet-stream" --data-binary @peca-canva.jpg "<upload_url>"
   ```
   A resposta traz `mediaId`. Cada URL serve uma vez só; se falhar, peça outra.
4. **Design de destino**, nesta ordem de preferência:
   a. Atualizar um design desta mesma peça que já exista (mesmo título/projeto) — `search-designs`.
   b. Copiar (`copy-design`) um design do usuário que já tenha **o mesmo tamanho** (confira com `read-design` → `page_metadata`) e limpar o conteúdo da cópia. O original não muda; avise que a cópia foi a base.
   c. `resize-design` de qualquer design para o tamanho em px (cria uma cópia), e limpar.
   d. Último recurso: `create-design` com um briefing simples no formato certo, e limpar.
5. **Montar** — `read-design` com `open_transaction: true`; apague os elementos (`delete_element`) ou, se houver um retângulo com imagem ocupando a página, use `update_fill` nele; insira/ajuste a imagem em `top 0, left 0, width W, height H`; `crop_media` com a caixa exata (W+0,6 × H se o Canva cortar 1 px); `update_title` com `<Marca> — <peça> (<L>x<A> cm)`.
6. **Aprovação** — mostre a miniatura devolvida pela edição e **peça confirmação antes de salvar** (`finalize: "commit"`). O conector exige isso; não salve sem um "sim".
7. Depois de salvo: dê o link de edição. Se a resposta do Canva indicar que o design pode ser impresso pelo Canva Print, mencione.

## Atualizar uma versão já enviada

Gere a nova imagem `--canva`, faça upload, e use `update_fill` + `crop_media` no mesmo elemento do mesmo design (na transação aberta, se ainda estiver ativa). Mostre a miniatura e peça aprovação de novo.
