---
name: teach
description: "Salva a identidade de marca (nome, logo, cores com contraste aprovado, fontes, contatos, obrigatórios) em .grafica.md para todas as peças impressas do plugin grafica. Use quando o usuário quiser cadastrar ou atualizar a marca para banners, flyers, cartões e afins."
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rasterizar.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/preflight.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_deps.py) Bash(pdftoppm *) Bash(pdftocairo *) Bash(pdfimages *) Bash(pdffonts *) Bash(pdfinfo *)"
license: "MIT (código e textos); fontes empacotadas sob SIL OFL 1.1 — ver LICENSE"
---

# /grafica:teach

**Pedido:** $ARGUMENTS
**Uso:** `/grafica:teach`

> **RAIZ** = pasta do plugin: `${CLAUDE_PLUGIN_ROOT}`. Se a variável não aparecer resolvida, use a pasta-base informada ao carregar esta skill e suba dois níveis; se você chegou aqui a partir de outra skill do plugin (ex.: craft → grill), use a mesma RAIZ dela. Antes de começar, leia `RAIZ/nucleo/principios.md` (princípios, ferramentas e padrão de entrega) e, uma vez por sessão, rode `python3 RAIZ/scripts/check_deps.py` (se faltar algo ou o Python tiver outro nome, siga `/grafica:setup` — `RAIZ/skills/setup/SKILL.md`).

Grava a identidade da marca em `.grafica.md` para que toda peça seguinte já saia com ela.

## Perguntas (pule o que já estiver no pedido, em anexos ou num `.grafica.md` existente)

1. **Nome da marca** como deve aparecer, e o **segmento** (ex.: churrascaria, clínica de estética, oficina mecânica).
2. **Público e tom** — três adjetivos (ex.: popular, direto, caloroso; ou premium, discreto, técnico).
3. **Logo** — peça o arquivo (PNG com fundo transparente, SVG ou PDF). Anote o caminho e se existe versão para fundo escuro.
4. **Cores** — hex se souber; se não, extraia do logo (cores dominantes com Pillow, ignorando fundo) e confirme com a pessoa. Rode `relatorio_cores` com as cores da marca + neutros e registre no arquivo **os pares que passam** (texto × fundo) e as versões ajustadas para texto (`ajustar_contraste`), para que toda peça use a marca sem perder legibilidade.
5. **Fontes** — se a marca tem fonte própria, peça o .ttf/.otf; senão escolha um par de `RAIZ/references/tipografia.md` coerente com o tom e confirme.
6. **Contatos padrão** — WhatsApp/telefone com DDD, @, site, endereço, horário.
7. **Obrigatórios e regras** — registro profissional (CRM, CRN, CREA, OAB), CNPJ, frases legais, coisas que nunca podem aparecer.

Use a ferramenta de múltipla escolha para tom e fontes quando disponível; o resto em texto.

## Arquivo

Salve `.grafica.md` na pasta de trabalho (ou na pasta conectada do usuário, se ele trabalha numa). Copie logos para `marca/` ao lado. Formato:

```markdown
# Marca — <Nome>
- Segmento: <...>
- Público: <...>
- Tom: <adjetivo>, <adjetivo>, <adjetivo>

## Cores
- Principal: #RRGGBB  (uso: fundos, títulos)
- Destaque: #RRGGBB   (uso: preço, selos, chamadas)
- Neutra clara: #RRGGBB
- Neutra escura: #RRGGBB
- Para texto sobre claro: #RRGGBB (principal ajustada, 4,5:1+)
- Pares aprovados: principal × neutra clara 8,2:1 · destaque × neutra escura 7,6:1 · …
- CMYK da marca (se houver manual): C.. M.. Y.. K..

## Fontes
- Títulos/impacto: <arquivo ou nome do kit>
- Texto/apoio: <...>

## Logo
- Fundo claro: marca/logo.png
- Fundo escuro: marca/logo-branco.png
- Área de proteção: altura do símbolo em volta

## Contatos padrão
- WhatsApp: (DD) 9XXXX-XXXX
- Instagram: @...
- Site: ...
- Endereço: ...
- Horário: ...

## Obrigatórios e regras
- ...
```

Se o ambiente não guarda arquivos entre conversas, entregue o `.grafica.md` ao usuário e diga para anexá-lo quando pedir a próxima peça.

## Fim

Mostre um resumo de 4–5 linhas do que ficou salvo e sugira `/grafica:craft <tipo>`.
