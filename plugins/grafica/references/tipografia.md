# Tipografia para impressos

## Fontes do kit (`assets/fonts/`, todas OFL, com acentos do português conferidos)

Use o nome do arquivo sem extensão no kit (ex.: `"Anton-Regular"`).

| Papel | Fontes | Uso |
|---|---|---|
| Impacto condensado | `Anton-Regular` · `BebasNeue-Regular` (só caixa-alta) · `BigShoulders-Bold` / `-Regular` | N1 e N2 de rua: preço, oferta, título. Muita letra em pouca largura |
| Impacto largo/pesado | `ArchivoBlack-Regular` · `Boldonse-Regular` · `EricaOne-Regular` | Palavra única gigante, selo, varejo popular |
| Slab (rústico, robusto) | `AlfaSlabOne-Regular` | Gastronomia rústica, oficina, construção, cervejaria |
| Sans de apoio | `Montserrat-Regular` / `-Bold` · `WorkSans-Regular` / `-Bold` · `InstrumentSans-Regular` / `-Bold` · `Outfit-Regular` / `-Bold` · `BricolageGrotesque-Bold` | N3, contatos, cartões, textos corridos |
| Serifa de display | `Gloock-Regular` · `YoungSerif-Regular` · `InstrumentSerif-Regular` / `-Italic` | Nome de marca, sofisticado, gastronomia de autor |
| Serifa de texto | `Lora-Regular` / `-Italic` | Cardápio, folder, texto mais longo |
| Script | `Pacifico-Regular` (casual); para o formal, `InstrumentSerif-Italic` grande | Só palavras curtas e GRANDES (≥ 2× a letra mínima). Nunca para informação |

`fontes_disponiveis()` lista também fontes do sistema. Fonte própria do cliente: `registrar_fonte("marca/Fonte.ttf")` — o kit recusa fonte variável (gere instância estática com `fontTools.varLib.instancer`) e avisa se faltar algum caractere (acentos!).

## Combinações prontas

| Contexto | Títulos | Apoio |
|---|---|---|
| Varejo / promoção / supermercado | Anton ou ArchivoBlack | Montserrat |
| Churrascaria / hamburgueria / bar | BigShoulders-Bold ou AlfaSlabOne | WorkSans ou InstrumentSans |
| Gastronomia de autor / café | Gloock ou YoungSerif | InstrumentSans; InstrumentSerif-Italic para frases |
| Saúde / estética / clínica | InstrumentSerif ou Gloock (nome) | Outfit ou WorkSans |
| Oficina / construção / serviços técnicos | ArchivoBlack ou AlfaSlabOne | Montserrat-Bold |
| Infantil / festa | Pacifico (palavra curta) + Outfit-Bold | Outfit |
| Igreja / eventos formais | Gloock ou YoungSerif | Lora |

Máximo de **duas famílias** por peça (três estilos no total). Contraste vem de tamanho e peso, não de mais fontes.

## Regras para distância

- À distância, o que lê é **peso e forma**: bold/black condensada para N1; regular para N3 de perto. Light/thin só em peça de mão e grande.
- Caixa-alta condensada lê bem até ~1,2:1 de proporção altura/largura da letra; mais apertada que isso vira grade de barras de longe — confira na simulação.
- **Tracking**: caixa-alta pequena (N3, rótulos) com +5 a +10 % do tamanho; títulos grandes com 0 a +3 %; números grandes ajustados par a par.
- **Kerning**: o kit não aplica kerning automático. Em textos grandes, olhe pares como `AV`, `To`, `R$`, `7,` `1 1` e ajuste com `tracking` ou separando em partes.
- Números em display com algarismos alinhados; centavos sobrescritos a ~45 % do inteiro; "R$" a ~25–30 % (o kit faz em `preco`).
- Caixa-alta em frase longa cansa: ok para N1/N2 curtos; N3 em caixa mista.
- Itálico só para frase de apoio curta (tagline, "por pessoa").

## Tamanhos em peças de mão (em pt, o que se usa no dia a dia)

Cartão: nome 9–11 pt · cargo/contatos 7–8 pt (nunca < 6,5 pt) · Flyer: título 28–60 pt · texto 9–11 pt · rodapé ≥ 7 pt. No kit use `pt=` nessas peças.
