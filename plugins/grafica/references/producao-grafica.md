# Produção gráfica

## Sangria e margem de segurança

- **Sangria**: área extra além do corte, onde fundos, fotos e cores chapadas continuam. A guilhotina/refile nunca é perfeita; sem sangria aparece um filete branco.
- **Margem de segurança**: distância mínima do corte para o que não pode ser cortado nem ficar escondido (textos, logo, contatos, QR).

| `material` | Sangria | Segurança | Por quê |
|---|---|---|---|
| `cartao` | 3 mm | 4 mm | corte em lote varia ~1 mm |
| `papel` (flyer, cartaz, folder, cardápio) | 3 mm | 5 mm | idem; folder: +2 mm perto das dobras |
| `adesivo` | 2 mm | 3 mm | recorte eletrônico |
| `pvc` (placa PVC/ACM) | 3 mm | 1 cm | furos de fixação |
| `lona`, `faixa` | 1 cm | 4 cm | ilhós a ~2 cm da borda, bainha, tensionamento |
| `outdoor` | 5 cm | 10 cm | colagem em folhas, emendas; siga o gabarito da exibidora |

O kit aplica esses valores pelo `material`; sobrescreva com `sangria=` / `seguranca=` quando a gráfica mandar outros.

## Acabamentos que comem área

- **Banner com bastão e cordão**: a lona dobra em volta do bastão — reserve 3–5 cm em cima e embaixo (aumente `seguranca` ou deixe só fundo ali).
- **Ilhós**: nos cantos e a cada ~50 cm, a ~2 cm da borda. Lona com ilhós: nada importante nos 4 cm da borda.
- **Bainha / solda**: 2–4 cm dobrados.
- **Roll-up**: a base esconde ~10–15 cm.
- **Wind banner**: a haste ocupa uma lateral inteira; use o gabarito do fornecedor.
- **Dobras (folder)**: painel interno 2–3 mm menor; nunca texto atravessando a dobra.

## Corte especial

- Adesivo recortado, cartão com cantos arredondados, tag: a gráfica pede uma **linha de corte vetorial** separada (geralmente uma cor especial com nome combinado, ex.: "CutContour" ou "Faca"). Desenhe-a com `linha`/`poligono` em cor de destaque numa página ou camada à parte e pergunte à gráfica o nome exato da cor.

## Marcas de corte

- Papel em gráfica tradicional: `Peca(..., marcas_corte=True)`.
- Gráficas online normalmente pedem **sem marcas, com sangria**, no gabarito delas.
- Lona/faixa/adesivo grande: sem marcas.

## Cor

- O kit trabalha em **RGB**. Impressão digital (lona, gráfica rápida) aceita bem. Offset e algumas gráficas exigem **CMYK**: cores vetoriais podem ser definidas em CMYK (`cor("cmyk(0,35,85,0)")`); fotos devem ser convertidas com o perfil ICC da gráfica (peça a eles).
- **Preto rico** em áreas grandes de fundo (offset): C40 M30 Y30 K100 — preto só K fica acinzentado. **Texto pequeno**: só K 100 (registro perfeito). Em lona digital a diferença é pequena.
- **Branco não é tinta**: em papel colorido, kraft ou vinil transparente, "branco" é a cor do material — exige impressão de branco (avise a gráfica).
- Sol desbota: lona exposta perde vermelhos e amarelos primeiro em meses.

## Fontes e arquivo

- O PDF do kit incorpora as fontes (subconjunto). Não converta texto em imagem.
- Gráficas pedem às vezes **PDF/X-1a**: o kit não gera PDF/X; na prática a maioria aceita o PDF comum com fontes incorporadas. Se exigirem, a gráfica converte ou o usuário exporta pelo Canva/Illustrator.
- Nome do arquivo sem acento e sem espaço ajuda o envio.

## Ficha técnica (para colar na mensagem à gráfica)

```
Peça: <tipo — título>
Tamanho final: <L × A cm> (<orientação>) · sangria de <x> em cada lado
Material: <ex.: lona 440 g / couchê 300 g / vinil adesivo>
Impressão: <4×0 | 4×4> · <digital | offset>
Acabamento: <ilhós a cada 50 cm | bastão e cordão | laminação fosca | verniz localizado | refile | recorte>
Cores: <RGB — converter com o perfil da gráfica | CMYK>
Arquivo: <nome.pdf> (fontes incorporadas; fotos a <n> dpi efetivos)
Quantidade: <a confirmar>
```
