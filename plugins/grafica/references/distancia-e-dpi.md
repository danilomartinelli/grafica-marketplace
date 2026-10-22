# Distância de leitura → letra e resolução

## As duas regras de letra

Medida = **altura da letra maiúscula** (cap height), em cm. É o que o kit chama de `cap`.

- **Letra mínima** (limite de legibilidade, olho normal): `cap ≥ distância_m × 0,28`
- **Letra de impacto** (lida de passagem, sem esforço — use para o N1): `cap ≥ distância_m × 0,83`

Equivalente à regra de sinalização "1 polegada de letra a cada 10 pés para impacto, 30 pés no limite". Funções no kit: `letra_minima_cm`, `letra_impacto_cm`, `distancia_legivel_m(cap)`.

| Distância | Exemplos | Letra mínima | Impacto (N1) | DPI recomendado | DPI mínimo de foto |
|---|---|---|---|---|---|
| 0,3–1 m | cartão, flyer, cardápio | 0,15 cm (~6–7 pt) | 0,3 cm | 300 | 240 |
| 1–3 m | cartaz, roll-up, vitrine | 0,3–0,85 cm | 0,8–2,5 cm | 200 | 120 |
| 3–10 m | banner na porta, placa de calçada | 0,85–2,8 cm | 2,5–8,3 cm | 150 | 72 |
| 10–30 m | faixa, fachada | 2,8–8,4 cm | 8,3–25 cm | 100 | 45 |
| 30 m+ | outdoor, empena | 8,4 cm+ | 25 cm+ | 50 | 20 |

Use a distância **de decisão** (de onde a pessoa precisa entender e decidir parar), não a mais curta possível. Para faixa do outro lado de uma avenida, é a largura da avenida.

Hierarquia prática: N1 ≥ impacto · N2 ≥ 1,5 × mínima · N3 ≥ mínima · abaixo disso, só `papel="detalhe"` (lido por quem já parou).

## Por que o DPI depende da distância

O olho resolve ~1 minuto de arco. Um ponto de 1/DPI polegada visto a uma distância d some quando fica menor que isso: DPI útil ≈ 87 ÷ distância_m (teórico). Na prática a tabela acima tem folga, porque as pessoas chegam mais perto do que o planejado.

- **Vetor** (textos, formas, gradientes do kit) é nítido em qualquer tamanho: o DPI importa para **fotos** e para os **arquivos de imagem** exportados.
- **Pedido explícito do usuário vence** (ex.: "200 × 80 cm a 300 dpi"). Faça, e informe o custo: 200 × 80 cm a 300 dpi = 23 622 × 9 449 px = 223 MP; a 100 dpi seriam 25 MP com o mesmo resultado visto da rua.

Tamanho de arquivo de imagem (pixels = cm ÷ 2,54 × dpi):

| Peça | 100 dpi | 150 dpi | 300 dpi |
|---|---|---|---|
| 9 × 5 cm | — | — | 1063 × 591 (0,6 MP) |
| A4 | — | 1240 × 1754 | 2480 × 3508 (8,7 MP) |
| 80 × 120 cm | 3150 × 4724 (15 MP) | 4724 × 7087 (33 MP) | 9449 × 14173 (134 MP) |
| 200 × 80 cm | 7874 × 3150 (25 MP) | 11811 × 4724 (56 MP) | 23622 × 9449 (223 MP) |
| 500 × 100 cm | 19685 × 3937 (78 MP) | — | — |

Com foto, exporte em JPEG (q 90–94). PNG só para peça 100 % vetorial.

## Simulação de distância

`rasterizar.py peca.pdf --simular <metros>` gera a peça com 1 pixel por minuto de arco (o que um olho 20/20 resolve) e amplia para você olhar. Regra: **o que não se lê na simulação não será lido na rua.** Use no `craft` (peças a mais de 3 m) e sempre no `critique`.

## QR code

Lado ≥ distância de escaneamento ÷ 10, e ≥ 1,5 cm. Peça de mão: o celular chega a ~20 cm → 2 cm basta. Peça de parede/rua: a pessoa se aproxima até ~1–2 m → 10–20 cm. QR em faixa a 15 m só faz sentido se houver lugar para a pessoa parar perto. Sempre com margem clara em volta (zona de silêncio) e alto contraste (escuro sobre claro).
