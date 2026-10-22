---
name: grill
description: "Entrevista o pedido de uma peça impressa (banner, faixa, flyer, cartão, cartaz, placa…) antes de produzir — uma pergunta por vez, sempre com resposta recomendada, percorrendo distância, tamanho, mensagem, dados, obrigatórios, marca e cor — e fecha um briefing.md. Use quando o usuário quer planejar ou detalhar uma peça impressa; craft e adapt já o executam."
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/rasterizar.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/preflight.py *) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_deps.py) Bash(pdftoppm *) Bash(pdftocairo *) Bash(pdfimages *) Bash(pdffonts *) Bash(pdfinfo *)"
license: "MIT (código e textos); fontes empacotadas sob SIL OFL 1.1 — ver LICENSE"
---

# /grafica:grill [peça]

**Pedido:** $ARGUMENTS
**Uso:** `/grafica:grill [peça] [descrição]`

> **RAIZ** = pasta do plugin: `${CLAUDE_PLUGIN_ROOT}`. Se a variável não aparecer resolvida, use a pasta-base informada ao carregar esta skill e suba dois níveis; se você chegou aqui a partir de outra skill do plugin (ex.: craft → grill), use a mesma RAIZ dela. Antes de começar, leia `RAIZ/nucleo/principios.md` (princípios, ferramentas e padrão de entrega) e, uma vez por sessão, rode `python3 RAIZ/scripts/check_deps.py`.

Entrevista que tira todas as dúvidas do pedido **antes** de produzir — no espírito do *grill-me* do Matt Pocock: uma pergunta por vez, sempre com uma resposta recomendada, percorrendo a árvore de decisões em ordem, até as duas partes terem o mesmo entendimento. Só então a peça é feita.

É o passo 2 do `craft` e do `adapt`. Sozinho (`/grafica:grill banner`), termina num `briefing.md` pronto para o `craft`.

## Como conduzir

- **Uma pergunta por vez, com recomendação.** Se houver ferramenta de perguntas de múltipla escolha: uma pergunta por chamada, a opção recomendada primeiro com "(Recomendado)", e uma linha dizendo *por que* (o que essa resposta muda na peça). Sem ela, faça o mesmo em texto: a pergunta, as opções numeradas com "(Recomendado)" na primeira, e "ou me diga outra coisa". Perguntas abertas (texto da oferta, dados) vão em texto, também uma por vez.
- **Descubra sozinho o que dá para descobrir.** Antes de perguntar, olhe: o próprio pedido, anexos, `.grafica.md`, peças anteriores na pasta, os padrões do tipo em `formatos.md`, as regras em `obrigatorios.md`, e a web quando for fato (regra da prefeitura, tamanho padrão de um suporte). Só decisões de verdade vão para o usuário.
- **Siga a ordem da árvore.** Uma decisão que depende de outra só é perguntada depois (o tamanho depende de onde fica; a letra depende da distância; a paleta depende da marca).
- **Não interrogue à toa.** Pule o que já foi respondido ou só tem uma resposta sensata — e registre como premissa no briefing. No caso típico são 4 a 8 perguntas; peça simples com pedido completo pode ter 1 ou 2.
- **"Decide você" encerra o grill**: complete o resto com as recomendações e vá para o briefing.
- **Sem ninguém para responder** (execução agendada, teste, `--rapido`): não pergunte; use as recomendações e liste-as no topo da entrega.

## A árvore (nesta ordem)

1. **Objetivo e público** — o que a peça precisa fazer acontecer (vender uma oferta, anunciar inauguração, apresentar um serviço, institucional) e quem passa por ela. Define o N1 e a energia.
2. **Onde vai ficar → distância de leitura.** Recomende pelo tipo e pelo lugar descrito ("no alto do portão, vista do outro lado da avenida" → rua, 10–30 m). Explique em meia frase: muda letra mínima e DPI.
3. **Tamanho, orientação, material e acabamento.** Ofereça os tamanhos comuns do tipo; pergunte acabamento só se mudar a área útil (bastão, ilhós, dobra, recorte) e se a gráfica tem gabarito próprio (gráfica online).
4. **A mensagem dos 3 segundos.** Proponha a frase (ex.: "Troca de óleo + filtro por R$ 129,90 na Oficina do Zé") e peça confirmação ou ajuste. É a decisão mais importante — não pule.
5. **Dados e condições.** Liste o que a peça precisa e pergunte só o que falta: preço, validade, limites, condições, contato (WhatsApp/telefone com DDD, @, site), endereço, horário. Nada inventado: o que não vier vira placeholder marcado.
6. **Obrigatórios do segmento** (`obrigatorios.md`): proponha incluir com o texto pronto (frase de descarte de panfleto, registro profissional, advertência de álcool, "imagens meramente ilustrativas").
7. **Marca e cor.** Com `.grafica.md`, só confirme. Sem: logo? cores da marca? Se não houver, proponha uma paleta pela psicologia do segmento e pelo contraste (`RAIZ/references/cor.md`) e peça um "ok".
8. **Imagem.** Fotos próprias (melhor), foto de banco com licença livre, ilustração vetorial ou tipografia-imagem. Recomende pelo segmento (comida e produto → foto).
9. **Energia.** Push (padrão de rua) · Equilibrado · Sofisticado — recomende pelo contexto.
10. **Entrega.** Gráfica pede CMYK? Vai para o Canva? Precisa de outros formatos depois (`adapt`)?

## Fechamento

Mostre o briefing e peça um "ok" antes de produzir:

```markdown
## Briefing — <peça> <marca>
- Peça: <tipo>, <L × A cm>, <orientação>, <material/acabamento>
- Leitura: <distância> → letra mínima <x> cm, impacto <y> cm, <dpi> dpi
- 3 segundos: "<frase>"
- Hierarquia: N1 <...> · N2 <...> · N3 <...>
- Conteúdo: <lista>; obrigatórios: <lista>; a conferir: <placeholders>
- Cor: <paleta e papéis; contraste-chave x:1>
- Imagem: <fonte e licença>
- Energia: <push/equilibrado/sofisticado> · Entrega: <PDF + JPG/PNG <dpi>, CMYK?, Canva?>
```

Salve como `briefing.md` na pasta da peça. Com o "ok", siga para o próximo passo do comando que chamou o grill.

## Exemplo de pergunta bem feita

> **De onde as pessoas vão ver a faixa?** Recomendo **do outro lado da avenida (10–30 m)** — é como você descreveu o portão. Isso pede letra de pelo menos 5,6 cm para o WhatsApp e preço com ~17 cm, e imagem a 100 dpi.
> ○ Do outro lado da avenida, 10–30 m (Recomendado) ○ Da calçada, 3–10 m ○ Bem perto, 1–3 m
