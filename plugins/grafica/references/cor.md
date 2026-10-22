# Cor: marca, psicologia, contraste e acessibilidade

Escolha cor nesta ordem — cada passo só decide o que o anterior deixou em aberto:

1. **Marca primeiro.** Se existe `.grafica.md` ou logo, as cores da marca mandam. Psicologia de cor nunca troca a cor de uma marca; ela só escolhe *como usar* (fundo, destaque, texto) e o que completa.
2. **Papéis.** Defina quem é fundo, quem é N1, qual é o destaque (uma cor só — preço, selo, ação) e qual é a cor do texto.
3. **Contraste e acessibilidade.** Cada par texto × fundo precisa passar. Se a cor da marca não passa como texto, **ajuste a luminosidade sem trocar o tom** em vez de abandoná-la.
4. **Psicologia e segmento** para completar a paleta quando não há marca (ou quando a marca só tem uma cor).

## 1. Usando as cores da marca

- **Marca saturada e média** (laranja `#F7931E`, amarelo, verde-limão, vermelho vivo): ótima como **campo de cor** (fundo, faixa, selo) ou letra **grande** sobre escuro. Como texto sobre claro ela falha. Escureça o tom para texto: `ajustar_contraste("#F7931E", "#F4EFE6", 4.5)` → `#A35B06` (mesmo laranja, mais queimado).
- **Marca escura** (azul-marinho, verde-garrafa, vinho): fundo nobre com texto claro, ou texto sobre fundos claros.
- **Marca clara/pastel**: fundo ou detalhe; texto sempre em neutro escuro.
- **Duas cores de marca vizinhas em luminância** (vermelho × verde, azul × roxo): nunca uma sobre a outra para texto — de longe e para daltônicos viram a mesma cor. Separe com branco/creme/preto.
- **Logo nunca é recolorido**: use a versão para fundo claro ou escuro que a marca tiver. Se o logo some no fundo planejado, mude o fundo atrás dele (faixa, área de respiro), não o logo.
- Antes de desenhar, rode `relatorio_cores({...})` com a paleta da marca + neutros: ele mostra todos os pares com o contraste normal e o pior caso com daltonismo, e diz para que cada par serve.

## 2. Contraste

- **Razão WCAG** (`contraste(c1, c2)`, de 1 a 21). Metas nesta skill:
  - **≥ 7:1** — N1 e N2 de peça de rua (luz do sol, movimento, distância, visão média de quem passa).
  - **≥ 4,5:1** — qualquer informação (contato, preço, condições), em qualquer peça.
  - **≥ 3:1** — só letras muito grandes ou grafismos que não carregam informação sozinhos.
- **De longe, quem lê é a luminância, não o matiz.** Duas cores vibrantes de mesma luminosidade (vermelho e verde, laranja e rosa) "brigam" de perto e somem de longe. Teste: a folha `rasterizar.py --daltonismo` traz a peça em tons de cinza — se a informação some no cinza, falta contraste de verdade.
- Texto sobre foto: o contraste depende da área da foto atrás do texto. Trate (fade, `escurecer`, faixa sólida) e confira na prévia e na simulação de distância.
- Pares fortes na rua: preto/amarelo · branco/vermelho escuro · creme/marrom-carvão · branco/azul-marinho · âmbar/carvão.
- Pares que falham: amarelo ou laranja claro sobre branco · vermelho sobre preto (escuro sobre escuro) · azul sobre preto · cinza médio sobre cor média · vermelho × verde.

## 3. Acessibilidade

- **Daltonismo** (~8 % dos homens, ~0,5 % das mulheres; o mais comum confunde vermelho e verde): nunca use **só a cor** para diferenciar informação (preço antigo × novo, aberto × fechado, item em promoção). Junte forma, posição, risco, ícone ou texto. Confira com `rasterizar.py --daltonismo`.
- **Baixa visão e público mais velho** (farmácia, clínica, igreja, comércio de bairro): aumente as letras ~25 % além da mínima, evite pesos finos e cinza claro, prefira contraste ≥ 7:1 mesmo em peças de mão.
- **Leitura fácil**: frases curtas, caixa-alta só em títulos curtos, sem itálico ou script para informação, números grandes e com separação clara (telefone com DDD, horário com "às").
- **Ícone + texto**: WhatsApp, endereço e horário reconhecidos pelo ícone *e* escritos.
- **QR code** sempre com a URL ou o contato também escritos (nem todo mundo escaneia).
- **Brilho**: laminação brilhante sob luz forte cria reflexo que apaga texto; para peça de mão muito usada (cardápio), prefira fosco.
- **Noite**: peça de fachada lida à noite precisa de iluminação ou material refletivo; fundos escuros com texto claro funcionam melhor sob luz artificial.

## 4. Psicologia das cores (para completar, não para substituir a marca)

Associações comuns no Brasil — dependem de contexto, cultura e concorrência; use como ponto de partida:

| Cor | Evoca | Funciona em | Cuidado |
|---|---|---|---|
| Vermelho | urgência, apetite, promoção, paixão | liquidação, fast food, açougue, selos | em excesso cansa; escuro sobre escuro some |
| Laranja | energia, preço acessível, amigável | varejo popular, delivery, infantil | como texto em fundo claro falha — use em campo |
| Amarelo | atenção, otimismo, alerta; a cor mais visível de longe | faixa, fachada, oficina, supermercado | nunca texto amarelo sobre branco; com preto é máximo contraste |
| Verde | saúde, natural, frescor, dinheiro | farmácia, orgânico, nutrição, sustentabilidade | verde × vermelho para daltônicos é igual |
| Azul | confiança, técnica, limpeza, calma | clínica, serviço técnico, banco, piscina | "frio" para comida; azul sobre preto some |
| Roxo | sofisticação, criatividade, místico | beleza, estética, eventos | pouco contraste com azul e vermelho |
| Rosa | cuidado, delicadeza, doce | confeitaria, estética, infantil | evite estereótipo de gênero sem motivo |
| Marrom/terra | rústico, artesanal, café, chocolate | padaria, café, churrasco, cervejaria | combine com creme ou âmbar para não ficar pesado |
| Preto | premium, força, noite | contraste máximo, hamburgueria, moda | grande área em offset pede preto rico |
| Branco/creme | limpeza, espaço, calma | respiro, saúde, sofisticado | branco puro em lona suja rápido; creme envelhece melhor |
| Dourado/ocre | premium, celebração, tradição | joalheria, eventos, gastronomia | dourado "metálico" não sai em CMYK — vira mostarda; use ocre |

Datas e contexto pesam: Natal (vermelho/verde/dourado), Junina (cores vivas, xadrez), Black Friday (preto/amarelo), Outubro Rosa / Novembro Azul. Evite cores associadas a partidos em período eleitoral quando não for o assunto.

### Paletas de partida por segmento (quando não há marca)

| Segmento | Fundo | Destaque | Apoio |
|---|---|---|---|
| Churrascaria / carnes | carvão `#140E0B` | âmbar `#FFA833`, vermelho `#C9341B` | creme `#F1E5D1` |
| Pizzaria / italiano | creme `#F4EBDD` ou verde `#1E4D2B` | vermelho tomate `#C8102E` | verde `#2E7D32` |
| Padaria / café | creme `#F3E9DC` | marrom `#6B3E26` | caramelo `#C58B4E` |
| Hamburgueria | preto `#111111` | amarelo `#FFC72C` | vermelho `#D62300` |
| Supermercado / varejo popular | amarelo `#FFD200` ou branco | vermelho `#E30613` | azul `#003DA5` |
| Saúde / clínica | branco `#FFFFFF` | verde-água `#2A9D8F` ou azul `#1D4E89` | grafite `#3A3F44` |
| Estética / beleza | nude `#F2E3DB` | rosé `#C97B84` ou ocre `#B8975A` | grafite `#2E2A28` |
| Oficina / construção | preto `#151515` | amarelo segurança `#FFCC00` | cinza `#9AA0A6` |
| Pet | branco ou azul claro `#E8F4FA` | laranja `#FF7F11` | azul `#1B4965` |
| Jurídico / contábil | azul-marinho `#14213D` | ocre `#C9A227` | off-white `#F5F3EE` |

Confirme sempre com `relatorio_cores` — algumas combinações acima só servem para letras grandes.

## 5. Cor na impressão

- O kit trabalha em RGB por padrão (gráfica rápida/digital aceita). Para offset ou gráfica que exige CMYK: `Peca(..., cores="cmyk")` converte vetores e fotos pelo perfil ICC (FOGRA39 se existir no sistema; `GRAFICA_ICC=/caminho/perfil.icc` para usar o da gráfica). Detalhes em `RAIZ/skills/export/SKILL.md`.
- RGB vivo cai em CMYK: verde-limão, azul elétrico, laranja e rosa neon, roxo vibrante. Prefira as versões "imprimíveis" (ex.: laranja `#F7931E` em vez de `#FF6A00`) e avise se a marca depende dessas cores (prova de cor).
- Uma cor de destaque, uma função. Se tudo é destaque, nada é.
- Lona ao sol desbota vermelhos e amarelos primeiro — para longa exposição, garanta contraste escuro × claro, não só cor × cor.
