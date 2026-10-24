# grafica — comunicação visual impressa

Plugin para criar, revisar e entregar peças **impressas**: banner, faixa, lona de fachada, wind banner, cartaz, flyer/panfleto, folder, cartão de visita, adesivo de vitrine, placa, cardápio, encarte e outdoor.

Tudo parte de quatro perguntas — **de onde vão ver, qual o tamanho, em que material, o que precisa ser entendido primeiro** — e sai pronto para a gráfica: PDF vetorial no tamanho real com sangria (RGB ou CMYK), imagem no DPI certo para a distância, prévia, manifesto de direção de arte e ficha técnica. Filho do *canvas-design*: herda a direção de arte e a artesania, troca o minimalismo de galeria pelo **formato push** (imagem forte, oferta gigante, selo, ação clara).

## Instalar

**App do Claude:** em **Personalização → Plugins**, clique em **Adicionar → Adicionar marketplace** (*Add marketplace*), cole `danilomartinelli/grafica-marketplace` e instale **Gráfica**. Depois, numa **Nova tarefa** do Cowork, digite `/grafica:setup`.

**Claude Code:**

```
/plugin install grafica --marketplace danilomartinelli/grafica-marketplace
```

(Versões antigas, sem `--marketplace`: `/plugin marketplace add danilomartinelli/grafica-marketplace` e depois `/plugin install grafica@grafica-marketplace`.) Depois, rode `/grafica:setup`.

Passo a passo para quem não é técnico, e um roteiro para o próprio Claude seguir: [INSTALAR.md](https://github.com/danilomartinelli/grafica-marketplace/blob/main/INSTALAR.md).

## Comandos

| Comando | O que faz |
|---|---|
| `/grafica:setup` | Prepara o computador na primeira vez: confere Python e bibliotecas, instala com a sua permissão e testa |
| `/grafica:teach` | Salva a identidade da marca (`.grafica.md`) — cores com contraste aprovado, fontes, logo, contatos |
| `/grafica:grill [peça]` | Entrevista o pedido: uma pergunta por vez, com recomendação, até fechar o briefing |
| `/grafica:craft <tipo>` | Cria uma peça nova (passa pelo grill, escreve a direção de arte, constrói, confere, exporta) |
| `/grafica:critique [arquivo]` | Crítica como quem passa na rua: 3 segundos, distância simulada, contraste, daltonismo |
| `/grafica:audit [arquivo]` | Pré-impressão: tamanho, sangria, margem, fontes, DPI, letra mínima, RGB × CMYK |
| `/grafica:polish` | Acabamento fino sem mudar o conceito |
| `/grafica:bolder` | Mais chamativo |
| `/grafica:quieter` | Mais sóbrio |
| `/grafica:photo` | Foto com licença livre, opacidade, fade-x, sombra atrás do texto |
| `/grafica:adapt <formato>` | Mesma peça em outro formato (banner → flyer → cartão → post) |
| `/grafica:export` | Arquivos finais (RGB ou CMYK pelo perfil ICC) + ficha para a gráfica |
| `/grafica:canva` | Sobe a peça para o Canva como design no tamanho real |

Exemplo: `/grafica:craft faixa 300x100 para a Oficina do Zé, troca de óleo por R$ 129,90, vista do outro lado da avenida`.

## O que vem dentro

- **Kit Python** (`scripts/grafica_kit.py`): monta a peça em cm reais, com sangria, marcas de corte, texto alinhado pela tinta, preço de varejo ("de R$ X por"), fotos com fade e sombra, QR code, modo CMYK, e checagens automáticas (sobreposição, margem de segurança, letra mínima para a distância, contraste, DPI).
- **Ferramentas**: `rasterizar.py` (DPI exato, versão Canva, prévia com guias, **simulação de distância**, **folha de daltonismo**), `preflight.py` (auditoria de qualquer PDF ou imagem), `check_deps.py`.
- **24 fontes OFL** com acentos do português conferidos, e referências de formatos brasileiros, distância × DPI, produção gráfica, composição, tipografia, cor (marca, psicologia, contraste, acessibilidade) e obrigatórios legais (CDC, panfleto de rua, conselhos profissionais).

## Requisitos

Python 3.9 ou mais novo com as bibliotecas de `requirements.txt` (reportlab, Pillow, fonttools, numpy, pypdf, pypdfium2). O `/grafica:setup` confere, mostra o que falta, instala com a sua permissão e testa gerando um cartão de exemplo. O poppler é opcional. Modo CMYK usa um perfil ICC: ponha o `.icc` da gráfica na pasta de trabalho (ou defina `GRAFICA_ICC`); sem isso, o kit usa o FOGRA39 ou um perfil CMYK genérico do sistema.

## O que o plugin executa, baixa e envia

- **Executa** só scripts Python locais da pasta `scripts/` e, se estiverem instaladas, as ferramentas do poppler (`pdftoppm`, `pdfimages`). Os scripts não acessam a rede e não instalam nada; `check_deps.py` apenas lista o que falta e o comando para resolver.
- **Instala** bibliotecas Python só no `/grafica:setup`, só as de `requirements.txt`, vindas do PyPI pelo `pip`, e só depois de você autorizar.
- **Baixa** fotos só quando você pede uma foto de banco (`/grafica:photo`): busca em bancos de licença livre (Unsplash, Pexels, Pixabay), confere a licença e salva numa pasta `fotos/` da sua pasta de trabalho.
- **Envia** a peça para fora só no `/grafica:canva`, e só para a **sua** conta do Canva, pelo conector do Canva que você mesmo conectou — com a sua aprovação antes de salvar o design.
- **Guarda** os dados da marca que você informar no `/grafica:teach` (nome, telefone, endereço, e-mail, redes) só no arquivo `.grafica.md` da sua pasta de trabalho; nada vai para servidor do plugin.
- Nenhuma telemetria, nenhum servidor próprio, nenhuma credencial lida do seu ambiente.

## Licenças

Código e textos: MIT. Fontes em `assets/fonts/`: SIL Open Font License 1.1 (licenças em `assets/fonts/licencas/`).
