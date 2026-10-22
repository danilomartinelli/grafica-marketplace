# Formatos de peça

Tamanhos comuns no mercado brasileiro (L × A, em cm), material padrão, distância típica de leitura e energia sugerida. Use como opções na entrevista do `craft` e como padrão quando o usuário não souber. **Sempre vale o gabarito da gráfica escolhida** quando ele existir.

`material` = valor para `Peca(material=...)` (define sangria e margem de segurança; ver `producao-grafica.md`).

## Peças de mão (até 1 m) — 300 dpi

| Tipo | Tamanhos comuns | material | Energia | Observações |
|---|---|---|---|---|
| Cartão de visita | **9 × 5** · 8,5 × 5,5 · 5,5 × 5,5 | `cartao` | sóbrio/equilibrado | Frente e verso; couchê 300 g; laminação fosca ou verniz localizado; QR ≥ 1,5–2 cm |
| Flyer / panfleto | **10 × 15** · 10 × 14 · 15 × 21 · A5 14,8 × 21 · A6 10,5 × 14,8 | `papel` | push/equilibrado | Frente = chamada, verso = informação; couchê 90–150 g |
| Folder | A4 aberto 29,7 × 21 com 2 dobras (3 painéis de ~9,9) · A4 com 1 dobra | `papel` | equilibrado | Painel que dobra para dentro 2–3 mm menor; nada atravessando a dobra |
| Cardápio | A4 · A3 dobrado · 1/3 de A4 (10 × 21) | `papel` | por segmento | Preços alinhados à direita, mesma coluna; plastificado se for de mesa |
| Encarte / tabloide | A4 · 28 × 42 | `papel` | push | Grade de produtos com preço gigante por item |
| Convite / postal | 15 × 21 · 10 × 15 | `papel` | sóbrio | |
| Ímã de geladeira | 7 × 10 · 5 × 9 | `papel` | equilibrado | Telefone/WhatsApp como N1 |
| Display de mesa | A6 · A5 · 10 × 15 | `papel` | equilibrado | |

## Peças de perto (1–3 m) — 150–200 dpi

| Tipo | Tamanhos comuns | material | Energia | Observações |
|---|---|---|---|---|
| Cartaz | A3 29,7 × 42 · A2 42 × 59,4 · 46 × 64 · A1 59,4 × 84,1 | `papel` | push | |
| Roll-up | 80 × 200 · 85 × 200 · 100 × 200 | `lona` | push | A base esconde ~10–15 cm embaixo: nada importante ali; leitura entre 1 m e 1,8 m de altura |
| X-banner | 60 × 160 · 80 × 180 | `lona` | push | Ilhós nos 4 cantos |
| Adesivo de vitrine | sob medida | `adesivo` | push | Recorte precisa de linha de corte vetorial; perfurado (one-way) perde nitidez em letras finas |
| Placa PVC/ACM | 20 × 30 · 30 × 40 · 40 × 60 · 60 × 90 | `pvc` | equilibrado | Furos nos cantos |

## Peças de calçada (3–10 m) — 100–150 dpi

| Tipo | Tamanhos comuns | material | Energia | Observações |
|---|---|---|---|---|
| Banner com bastão e cordão | 60 × 90 · 80 × 120 · 90 × 120 · 100 × 150 (vertical) | `lona` | push | Bastão come ~3–5 cm em cima e embaixo |
| Wind banner / bandeira | alturas de 2,5 a 4,5 m (formato "pena"/"gota") | `lona` | push | **Use o gabarito do fornecedor** — a forma varia; texto na vertical, perto da haste fica escondido |
| Cavalete / placa de calçada | 60 × 90 · 50 × 70 | `pvc` | push | Frente e verso |

## Peças de rua (10–30 m) — 72–100 dpi

| Tipo | Tamanhos comuns | material | Energia | Observações |
|---|---|---|---|---|
| Faixa | 300 × 70 · 300 × 100 · 400 × 100 · 500 × 100 | `faixa` | push | Uma frase + marca + contato; ilhós a cada ~50 cm |
| Lona de fachada / banner horizontal | 200 × 80 · 300 × 100 · sob medida | `lona` | push | Confirme se vai em estrutura (tensionada) ou com ilhós |
| Placa de fachada / letreiro | sob medida | `pvc` / `lona` | por segmento | Nome da marca é o N1 |

## Peças de longe (30 m+) — 20–50 dpi

| Tipo | Tamanhos comuns | material | Energia | Observações |
|---|---|---|---|---|
| Outdoor (32 folhas) | 900 × 300 | `outdoor` | push | Arte pela proporção 3:1 com o gabarito da exibidora; no máximo ~7 palavras |
| Empena / front-light | sob medida | `outdoor` | push | |

## Digital (só via `adapt`)

| Tipo | Pixels | Como montar |
|---|---|---|
| Post Instagram retrato | 1080 × 1350 | `Peca(..., 10.8, 13.5, sangria=0)` + `rasterizar.py --dpi 254` |
| Story / Reels | 1080 × 1920 | `Peca(..., 10.8, 19.2, sangria=0)`; evite os 250 px de cima e de baixo |
| Post quadrado | 1080 × 1080 | `Peca(..., 10.8, 10.8, sangria=0)` |
