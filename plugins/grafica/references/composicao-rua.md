# Composição para peças impressas

## O teste dos 3 segundos

Quem passa a pé olha uma peça por 1–3 segundos; de carro, menos. Nesse tempo cabe: **uma imagem, uma frase curta, um número** — e o reconhecimento de quem está falando. Antes de desenhar, escreva a frase que a peça precisa deixar na cabeça (ex.: "Rodízio no almoço por R$ 99,99 no Tição"). Tudo que não serve a essa frase é N3 ou sai.

## Hierarquia em três níveis

- **N1** — o gancho: oferta, preço, produto, palavra-chave. Um elemento só. Em peça de rua ocupa 30–50 % da altura.
- **N2** — contexto: o que é (rodízio do almoço), de quem é (marca), a imagem.
- **N3** — ação e detalhes: contato, endereço, horário, condições. Lido por quem parou.

Saltos claros entre níveis (cada nível ≥ 1,6× o de baixo). Dois elementos do mesmo tamanho disputando o N1 = hierarquia quebrada.

## Padrões de layout que funcionam

1. **Foto + oferta** (varejo, gastronomia, serviços visuais). Foto protagonista ocupando ~50–60 % de um lado, sangrando nas bordas, com fade em direção ao bloco de texto (`fades=("direita", …)`); oferta alinhada à margem do outro lado. Marca no canto superior sobre área escura da foto (com `escurecer`).
2. **Tipográfico gigante** (liquidação, inauguração, aviso). Uma palavra ou número ocupando a peça de borda a borda da área útil; fundo chapado; nada de foto ou foto muito sutil.
3. **Selo / faixa de cor** (promoção). Etiqueta sólida com a palavra-gatilho no topo do bloco, ou faixa diagonal num canto. Um só por peça.
4. **Eixo central** (cartão, institucional, convite). Tudo alinhado ao centro com muito respiro; funciona em formatos pouco alongados. Em peça muito horizontal (3:1+), centralizar tudo vira uma linha fina perdida — prefira dois blocos.
5. **Grade de itens** (encarte, cardápio, tabela de preços). Colunas iguais, preço sempre no mesmo lugar e na mesma cor de cada célula, foto do item acima.
6. **Frente chamada / verso informação** (flyer, cartão). Frente = padrão 1 ou 2; verso = lista organizada, mapa ou QR.

## Peças muito horizontais (faixa, lona 3:1, outdoor)

O olho lê da esquerda para a direita: marca/imagem à esquerda, oferta no meio-direita, ação na ponta direita. Uma linha de leitura principal — nunca parágrafo. Altura útil é pouca: maximize letras em caixa-alta condensada.

## Peças verticais (banner com bastão, roll-up, wind banner)

Leitura de cima para baixo, na altura dos olhos (1–1,8 m do chão). Marca no topo, N1 na faixa dos olhos, ação embaixo mas acima da base/bastão.

## Níveis de energia

| | Push | Equilibrado | Sofisticado |
|---|---|---|---|
| Quando | rua, varejo, promoção, comida, evento popular | serviços, comércio de bairro, eventos | saúde, jurídico, arquitetura, moda, joalheria, cartão |
| Contraste fundo × N1 | máximo (≥ 10:1) | alto (≥ 7:1) | alto, mas com cores mais suaves |
| Cores | 1 neutro escuro/claro + 1–2 quentes saturadas | marca + 1 destaque | marca + neutros, destaques terrosos/metálicos |
| Tipografia N1 | display condensada pesada | sans bold / serifa bold | serifa de display ou sans regular com tracking |
| Foto | protagonista, opacidade 0,8–1 | presente, 0,6–0,9 | atmosfera 0,3–0,7, ou nenhuma |
| Ornamentos | selo sólido, faixa | fio, ícone simples | fio fino, nada |
| N1 ocupa | 30–50 % da altura | 20–35 % | 10–25 % |

Padrão por tipo em `formatos.md`. Na dúvida em peça de rua, vá de "Push" — o erro mais comum é ficar fraco, não forte demais (ver `direcao-de-arte.md`).

## Respiro e grade

- Margens internas generosas além da margem de segurança; o vazio deve parecer escolhido.
- Espaço entre grupos > espaço dentro do grupo.
- Alinhe tudo a 1–2 eixos (margem esquerda do bloco, margem direita da área útil). Medir com o kit: `medir`, `area_util`.
