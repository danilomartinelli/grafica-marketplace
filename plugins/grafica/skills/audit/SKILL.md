---
name: audit
description: "Pré-impressão (preflight) de um arquivo que vai para a gráfica: está pronto? por que a gráfica recusou? Confere tamanho final, sangria, margem de segurança, fontes incorporadas, DPI efetivo das fotos, letra mínima para a distância e RGB × CMYK, em PDF ou imagem."
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rasterizar.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/preflight.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_deps.py) Bash(pdftoppm *) Bash(pdftocairo *) Bash(pdfimages *) Bash(pdffonts *) Bash(pdfinfo *)"
license: "MIT (código e textos); fontes empacotadas sob SIL OFL 1.1 — ver LICENSE"
---

# /grafica:audit [arquivo]

**Pedido:** $ARGUMENTS
**Uso:** `/grafica:audit [arquivo] [--largura --altura --distancia]`

> **RAIZ** = pasta do plugin: `${CLAUDE_PLUGIN_ROOT}`. Se a variável não aparecer resolvida, use a pasta-base informada ao carregar esta skill e suba dois níveis; se você chegou aqui a partir de outra skill do plugin (ex.: craft → grill), use a mesma RAIZ dela. Antes de começar, leia `RAIZ/nucleo/principios.md` (princípios, ferramentas e padrão de entrega) e, uma vez por sessão, rode `python3 RAIZ/scripts/check_deps.py` (se faltar algo ou o Python tiver outro nome, siga `/grafica:setup` — `RAIZ/skills/setup/SKILL.md`).

Pré-impressão técnica: o arquivo vai sair da gráfica como esperado? Não opina sobre estética (isso é `critique`).

## Rodar

```bash
python3 RAIZ/scripts/preflight.py ARQUIVO [--largura CM --altura CM] [--distancia M] [--material lona|papel|cartao|adesivo|pvc|faixa|outdoor]
```

- Peças feitas pelo kit têm `.spec.json` ao lado: o preflight lê tudo de lá.
- Arquivos de fora: pergunte (ou deduza do pedido) tamanho final, distância e material; sem tamanho, a checagem de DPI fica incompleta — diga isso.
- Gere também `python3 RAIZ/scripts/rasterizar.py ARQUIVO --previa --guias` (se for PDF com caixas) e **olhe**: texto encostando na linha magenta, elementos cortados, foto pixelada.

## O que o preflight cobre

Tamanho final (TrimBox) e orientação · sangria contra o material · fontes incorporadas · resolução efetiva de cada imagem contra a distância · menor e maior letra contra a distância · textos começando dentro da margem de segurança · imagens RGB × CMYK (se a gráfica exige CMYK e a peça é do kit, refaça com `Peca(..., cores="cmyk")`).

## O que conferir à mão (o script não vê)

- **Bastão/ilhós/bainha**: banner com bastão perde ~3–5 cm em cima e embaixo; ilhós ficam a ~2 cm da borda a cada ~50 cm. Nada importante ali.
- **Dobras** (folder): texto atravessando dobra; painel interno 2–3 mm menor.
- **Recorte especial** (adesivo): existe linha de corte vetorial separada? Fale com a gráfica sobre o nome da cor de corte.
- **Preto**: fundos grandes pretos em offset ficam acinzentados com só K — gráfica costuma pedir preto rico; texto pequeno deve ser só K. (Em impressão digital/rápida isso pesa menos.)
- **Cores de marca** críticas (vermelho Coca, azul institucional): avise que RGB → CMYK muda; peça prova de cor se for importante.
- **Textos**: telefone com DDD, @ correto, sem erro de acento, placeholders esquecidos (`(XX)`, `XXXX`, "Lorem").
- **Lado > 8000 px**: só importa para entrega no chat (zipar).

## Entregar

O relatório com ✓ / ! / ✗, depois **o que corrigir** em linguagem de gráfica (ex.: "aumentar a sangria para 1 cm", "o telefone está a 2 cm da borda, dentro da área do ilhós"). Se a peça é do kit, ofereça corrigir e reexportar. Se é do usuário (imagem achatada), diga o que dá para corrigir e o que exige o arquivo aberto.
