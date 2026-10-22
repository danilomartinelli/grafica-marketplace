---
name: craft
description: "Cria, faz ou monta uma peça gráfica IMPRESSA nova — banner, faixa, lona de fachada, wind banner, cartaz, flyer/panfleto, folder, cartão de visita, adesivo, placa, cardápio, encarte, outdoor — no tamanho real em cm, com letra e DPI pela distância de leitura, sangria, cores da marca com contraste e acessibilidade e formato push para rua, entregando PDF vetorial (RGB ou CMYK) + imagem para a gráfica. Use sempre que pedirem para criar algo para imprimir ou pendurar na rua, loja, vitrine ou evento, mesmo sem dizer impresso. Não use para designs dentro do Canva (skills do Canva), pôster artístico (canvas-design), slides, documentos ou posts de rede social."
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rasterizar.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/preflight.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_deps.py) Bash(pdftoppm *) Bash(pdftocairo *) Bash(pdfimages *) Bash(pdffonts *) Bash(pdfinfo *)"
license: "MIT (código e textos); fontes empacotadas sob SIL OFL 1.1 — ver LICENSE"
---

# /grafica:craft <tipo>

**Pedido:** $ARGUMENTS
**Uso:** `/grafica:craft <tipo> [descrição livre]`

> **RAIZ** = pasta do plugin: `${CLAUDE_PLUGIN_ROOT}`. Se a variável não aparecer resolvida, use a pasta-base informada ao carregar esta skill e suba dois níveis; se você chegou aqui a partir de outra skill do plugin (ex.: craft → grill), use a mesma RAIZ dela. Antes de começar, leia `RAIZ/nucleo/principios.md` (princípios, ferramentas e padrão de entrega) e, uma vez por sessão, rode `python3 RAIZ/scripts/check_deps.py`.

Cria uma peça nova do zero até os arquivos prontos para a gráfica.

`<tipo>` costuma ser: banner, faixa, lona/fachada, wind-banner, cartaz, flyer/panfleto, folder, cartao, adesivo, placa, cardapio, encarte, outdoor. Se vier outra coisa, ache o mais parecido em `RAIZ/references/formatos.md`. `--rapido` pula as perguntas e usa as recomendações.

## 1. Carregar o que já se sabe

- Marca: `.grafica.md` (ver `RAIZ/nucleo/principios.md`) — cores, fontes, logo, contatos, regras.
- O próprio pedido e os anexos: muitas vezes já trazem tamanho, distância e conteúdo.
- O tipo em `RAIZ/references/formatos.md`: tamanhos padrão, material, distância típica e energia sugerida.

## 2. Grill — tirar as dúvidas antes de produzir

Siga a skill `/grafica:grill` (`RAIZ/skills/grill/SKILL.md`): uma pergunta por vez, com resposta recomendada, percorrendo a árvore (objetivo → distância → tamanho/material → mensagem dos 3 segundos → dados e condições → obrigatórios → marca e cor → imagem → energia → entrega), descobrindo sozinho o que for fato. Feche com o `briefing.md` e o "ok" do usuário.

As três perguntas que nunca ficam sem resposta (perguntadas ou registradas como premissa): **de onde vão ver** (distância → letra e DPI), **tamanho**, e **o que a peça precisa dizer**.

## 3. Cor

Siga `RAIZ/references/cor.md` nesta ordem: **cores da marca primeiro** → papéis (fundo, N1, destaque, texto) → **contraste e acessibilidade** → psicologia do segmento só para completar o que a marca não define. Use `relatorio_cores({"marca": "#C8102E", "creme": "#F4EBDD", ...})` para ver os contrastes entre as cores da paleta e `ajustar_contraste(cor, fundo, alvo)` para escurecer/clarear uma cor da marca sem trocar o tom até o texto passar.

## 4. Direção de arte (herança do canvas-design)

Leia `RAIZ/references/direcao-de-arte.md` e escreva o manifesto curto da peça em `direcao-de-arte.md` (6–10 linhas): nome do movimento, frase dos 3 segundos, como a peça faz o **push** de longe, matéria e cor (com o porquê de cada cor), forma e ritmo, **detalhe de assinatura** para quem se aproxima, cuidados de artesania.

Complete com o plano técnico:
- **N1 / N2 / N3:** o que é cada nível (ex.: N1 preço · N2 "rodízio do almoço" + marca · N3 horário, endereço).
- **Layout:** padrão de `composicao-rua.md` (em peça de rua, quase sempre "foto + oferta" ou "tipográfico gigante").
- **Tamanhos-alvo:** letra mínima e de impacto para a distância (`distancia-e-dpi.md`). N1 ≥ impacto; N2 ≥ 1,5 × mínima; N3 ≥ mínima; abaixo disso só `papel="detalhe"`.

## 5. Imagem e logo

- No formato push a peça começa pela imagem: foto real (a skill `/grafica:photo` (`RAIZ/skills/photo/SKILL.md`): fonte, licença, DPI efetivo, tratamento) para comida, produto, lugar e serviço; ilustração vetorial grande desenhada com o kit (formas, ícone construído, padrão) quando foto não cabe; ou tipografia-imagem (o número/palavra como elemento gráfico gigante). Peça de rua só com texto pequeno sobre fundo liso precisa de motivo.
- Logo do cliente: use o arquivo dele (PNG com transparência). Sem logo, a marca vira tipografia bem escolhida — não invente símbolo.

## 6. Construir com o kit

1. Copie `RAIZ/scripts/exemplo_banner.py` ou `RAIZ/scripts/exemplo_cartao.py` (o mais parecido) para a pasta de trabalho como `build_<peca>.py`. Rode sempre com o kit no caminho: `PYTHONPATH=RAIZ/scripts python3 build_<peca>.py`.
2. Defina no topo: medidas, material, distância, paleta, fontes (2 famílias, no máximo 3 estilos). Para gráfica que exige CMYK: `Peca(..., cores="cmyk")`.
3. Ordem que evita retrabalho: **fundo → medir os blocos (`medir`, `cap_para_largura`, `preco(..., desenhar=False)`) → foto (com `escurecer` atrás dos textos que ficam sobre ela) → grafismos → textos → `salvar()`**.
4. Dê `nome=` a todo texto e bloco importante; `sobre=` quando um texto fica de propósito em cima de uma forma (etiqueta); `papel="detalhe"` para o que é só de perto; `fundo=` nos textos-chave para o kit checar o contraste.
5. Posicione a partir de `p.area_util` (margem de segurança).

## 7. Checar e olhar (não pule)

1. `salvar()` imprime o relatório e os PROBLEMAS. Corrija até "nenhum" — ou justifique cada um que ficar.
2. `python3 RAIZ/scripts/rasterizar.py peca.pdf --previa --guias` e **abra a imagem**: alinhamentos, respiros, texto sobre área confusa da foto, nada encostando na linha magenta.
3. Peças vistas a mais de 3 m: `python3 RAIZ/scripts/rasterizar.py peca.pdf --simular <distância>` e abra. A frase dos 3 segundos tem que ser lida ali.
4. Acessibilidade de cor: `python3 RAIZ/scripts/rasterizar.py peca.pdf --daltonismo` (deuteranopia, protanopia, tritanopia e tons de cinza numa folha só) e abra. Se alguma informação some ou depende só de cor, corrija.
5. **Segunda passada (canvas-design):** pergunte "como deixar o que já existe mais preciso e mais forte?" — escala, alinhamento, respiro, contraste, o detalhe de assinatura. Não acrescente elementos novos nessa passada. Depois olhe como quem passa na rua: o primeiro olhar cai no N1?
6. `python3 RAIZ/scripts/preflight.py peca.pdf` e resolva todo ✗.

## 8. Exportar e entregar

Siga a skill `/grafica:export` (`RAIZ/skills/export/SKILL.md`) (PDF + imagem no DPI + prévia + `direcao-de-arte.md` + ficha para a gráfica). Na mensagem final: tamanho, material, DPI, placeholders a conferir, e um próximo passo (`critique`, `bolder`, `adapt` para outro formato, ou `canva`).
