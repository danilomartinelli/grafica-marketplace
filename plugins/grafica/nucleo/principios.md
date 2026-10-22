# Núcleo do plugin grafica — princípios, ferramentas e entrega

`RAIZ` = a pasta do plugin (onde está este arquivo, um nível acima de `nucleo/`).

Peça impressa é um objeto físico, visto **a uma distância**, por alguém **em movimento**, durante **poucos segundos**. Quase tudo aqui deriva de quatro perguntas: de onde vão ver, qual o tamanho, em que material, e o que precisa ser entendido primeiro. Web e tela seguem outras regras; não as traga para cá.

**Linhagem:** este plugin é filho do **canvas-design**. Herda o método — direção de arte escrita antes de desenhar, artesania de mestre, segunda passada que refina sem acrescentar — e troca o minimalismo de galeria pelo **formato push**: imagem forte, oferta gigante, selo, ação clara. Detalhes em `RAIZ/references/direcao-de-arte.md`.

## Os comandos (cada um é uma skill deste plugin)

| Comando | Para quê |
|---|---|
| `/grafica:teach` | Salvar a identidade da marca (nome, logo, cores, fontes, contatos) para todas as peças |
| `/grafica:grill [peça]` | Entrevistar o pedido até não sobrar dúvida (uma pergunta por vez, com recomendação) e fechar o briefing |
| `/grafica:craft <tipo>` | Criar uma peça nova (banner, faixa, cartao, flyer, cartaz, adesivo, placa, cardapio…) — começa pelo grill |
| `/grafica:critique [arquivo]` | Avaliar o design como quem passa na rua: 3 segundos, hierarquia, distância, cor e acessibilidade |
| `/grafica:audit [arquivo]` | Pré-impressão técnica: tamanho, sangria, margem, fontes, DPI, letra mínima |
| `/grafica:polish` | Acabamento fino sem mudar o conceito |
| `/grafica:bolder` | Deixar mais chamativo (push) |
| `/grafica:quieter` | Deixar mais sóbrio/elegante |
| `/grafica:photo` | Colocar/trocar foto (fonte licenciada, opacidade, fade, recorte) |
| `/grafica:adapt <formato>` | Transformar a peça em outro formato (banner → flyer → cartão → post) — também começa pelo grill |
| `/grafica:export` | Gerar os arquivos finais (RGB ou CMYK) e a ficha para a gráfica |
| `/grafica:canva` | Subir a peça para o Canva como design |

Pedido sem comando mas com intenção clara ("faz um banner pra minha loja") → é `craft`. Comandos encadeiam: `grill → craft → critique → bolder/polish → audit → export → canva`. Ao terminar, sugira o próximo passo que faz sentido (um só).

**Comandos de confecção (`craft`, `adapt`) sempre passam pelo grill antes de produzir**: tirar as dúvidas custa uma ou duas perguntas; refazer uma peça impressa custa dinheiro. `--rapido`, "decide você" ou uma execução sem ninguém para responder pulam as perguntas — aí as recomendações viram premissas listadas no topo da entrega.

## Antes de qualquer comando: a marca

Procure `.grafica.md` na pasta de trabalho (e nas pastas conectadas do usuário). Se existir, leia e use: cores, fontes, logo, contatos e regras valem para toda peça. Se não existir e o comando precisa de marca, pergunte só o mínimo dentro do próprio comando e, no fim, ofereça o `teach` para não repetir na próxima vez.

## Princípios que valem em todos os comandos

1. **A distância manda.** Altura de maiúscula mínima ≈ distância × 0,28 cm/m; para impacto (ler de passagem, sem esforço) ≈ distância × 0,83 cm/m. A resolução das fotos também vem da distância. Tabela completa e fórmulas: `RAIZ/references/distancia-e-dpi.md`.
2. **Uma mensagem, entendida em 3 segundos.** Quem passa precisa captar *o quê*, *quanto/por quê* e *de quem*. No máximo três níveis de hierarquia visíveis à distância de projeto; o resto é detalhe para quem se aproxima.
3. **Push por padrão, visual primeiro.** Peça de rua, loja e evento popular nasce no formato push: imagem protagonista (foto, ilustração grande ou tipografia-imagem), oferta gigante, selo, ação clara. Minimalismo de galeria em peça de rua parece vazio e não vende — erro real que um usuário corrigiu ("ficou muito minimalista para propaganda de rua"). Sobriedade só quando o contexto pede (cartão, saúde, jurídico) ou o usuário pede (`quieter`). Veja `RAIZ/references/direcao-de-arte.md` e `RAIZ/references/composicao-rua.md`.
4. **Tamanho real, produção real.** Trabalhe em cm reais, com sangria e área de segurança do material (`RAIZ/references/producao-grafica.md`). Ilhós, bastão, dobra e corte comem bordas: nada importante perto delas.
5. **Nada inventado sem aviso.** Telefone, endereço, horário, preço, CNPJ, registro profissional: só o que o usuário deu. Se faltar e a peça precisar, use um placeholder óbvio e liste-o na entrega para ele conferir.
6. **Cor: marca primeiro, depois contraste e acessibilidade.** As cores da marca mandam; a psicologia das cores só completa. Todo texto-chave passa no contraste (≥ 7:1 na rua, ≥ 4,5:1 sempre) — se a cor da marca não passa, ajuste a luminosidade mantendo o tom (`ajustar_contraste`). Nenhuma informação depende só de cor (daltonismo). Ver `RAIZ/references/cor.md`.
7. **Direitos e obrigatórios.** Fotos do cliente ou de banco com licença comercial livre (com crédito anotado); fontes do kit (todas OFL); nada de marcas, personagens ou logos de terceiros. Validade de oferta, registro profissional, frase de descarte de panfleto e afins: `RAIZ/references/obrigatorios.md`.
8. **Olhe antes de entregar.** Toda peça passa pelas checagens do kit, por uma prévia com guias, pela simulação de distância e pela folha de daltonismo — e você olha as imagens de verdade, como quem passa na rua.

## Ferramentas

Scripts em `RAIZ/scripts/` (Python 3 com reportlab, Pillow, fontTools, numpy, pypdf; poppler para `pdftoppm`, `pdfimages`, `pdffonts`):

- `grafica_kit.py` — biblioteca para montar a peça como **PDF vetorial no tamanho final** em cm: `Peca(...)`, `fundo`, gradientes, formas, `texto` (alinhamento pela tinta real, `cap=` em cm ou `pt=`), `paragrafo`, `preco` (R$ pequeno, inteiro gigante, centavos sobrescritos, "de R$ X por"), `foto` (cover, foco, opacidade, fades, sombra atrás de textos), `imagem` (logo), `qrcode`, `nova_pagina` (verso), `Peca(..., cores="cmyk")` (conversão pelo perfil ICC). Cor: `contraste`, `ajustar_contraste`, `relatorio_cores`, `simular_cor`. Texto gigante vira curvas sozinho (com camada pesquisável). `salvar()` grava o PDF + `<nome>.spec.json` e checa sobreposição, margem de segurança, letra mínima para a distância, contraste e DPI das fotos. Leia a docstring do módulo antes de usar.
- `exemplo_banner.py` (lona a 15 m com foto, fade e preço) e `exemplo_cartao.py` (cartão frente e verso com marcas de corte e QR) — copie para a pasta de trabalho como ponto de partida; não escreva do zero. A cópia roda com `PYTHONPATH=RAIZ/scripts python3 build_<peca>.py`.
- `rasterizar.py` — imagem no DPI certo e tamanho exato em pixels (`--dpi`, `--canva`, `--previa --guias`, `--simular <metros>`, `--daltonismo`, `--pagina`).
- `preflight.py` — auditoria de qualquer PDF ou imagem (com ou sem `.spec.json`).

As fontes empacotadas estão em `RAIZ/assets/fonts/` (com licenças) e o mapa de quando usar cada uma em `RAIZ/references/tipografia.md`. Fonte da marca do cliente: `registrar_fonte(caminho)`.

Rode os scripts com `python3 RAIZ/scripts/<script>.py` (dependências: `RAIZ/requirements.txt` + poppler; confira com `check_deps.py`). Trabalhe na pasta de trabalho do usuário, nunca dentro da pasta do plugin.

## Referências (`RAIZ/references/`, leia quando o comando pedir)

- `RAIZ/references/direcao-de-arte.md` — herança do canvas-design, formato push, manifesto da peça, segunda passada
- `RAIZ/references/formatos.md` — tipos de peça, tamanhos padrão no Brasil, material, distância típica, energia sugerida
- `RAIZ/references/distancia-e-dpi.md` — letra mínima, impacto, DPI, tamanho de arquivo, QR code
- `RAIZ/references/producao-grafica.md` — sangria, segurança, ilhós, bastão, dobras, corte especial, cores, ficha técnica
- `RAIZ/references/composicao-rua.md` — teste dos 3 segundos, hierarquia, padrões de layout, níveis de energia
- `RAIZ/references/tipografia.md` — fontes do kit por papel, combinações, regras para distância
- `RAIZ/references/cor.md` — marca primeiro, contraste, acessibilidade e daltonismo, psicologia das cores, paletas por segmento, CMYK
- `RAIZ/references/obrigatorios.md` — oferta e preço (CDC), panfleto de rua, profissionais de saúde, álcool, imóveis, direitos de imagem
- `RAIZ/references/anti-padroes.md` — o que não fazer e por quê

## Entrega (padrão de todos os comandos que geram arquivo)

Entregue os arquivos com uma linha de contexto cada, sem descrever o que a pessoa vai ver ao abrir:
1. **PDF para a gráfica** (vetorial, tamanho final, sangria, fontes incorporadas).
2. **Imagem no DPI da peça** (JPEG se tiver foto; PNG se for só vetor). Lado > 8000 px não pré-visualiza no chat: entregue zipado.
3. **Prévia** em PNG leve.
4. **`direcao-de-arte.md`** — o manifesto da peça (como o canvas-design entrega sua filosofia) e o `briefing.md` do grill.
Depois, em poucas linhas: o tamanho/material/DPI, os placeholders a conferir, qualquer limitação (ex.: foto com DPI no limite) e **um** próximo passo sugerido.
