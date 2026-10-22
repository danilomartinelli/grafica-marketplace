---
name: photo
description: "Coloca ou troca a foto de uma peça impressa: escolhe foto do cliente ou de banco com licença comercial livre, confere a resolução efetiva para a distância e trata com recorte, opacidade, fade-x e sombra atrás do texto. Use quando pedirem foto, imagem de fundo ou fade numa peça para imprimir."
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/*) Bash(pdftoppm *) Bash(pdftocairo *) Bash(pdfimages *) Bash(pdffonts *) Bash(pdfinfo *)"
license: "MIT (código e textos); fontes em RAIZ/assets/fonts sob SIL OFL 1.1"
---

# /grafica:photo

**Pedido:** $ARGUMENTS
**Uso:** `/grafica:photo [peça] [o que mostrar]`

> **RAIZ** = pasta do plugin: `${CLAUDE_PLUGIN_ROOT}`. Se a variável não aparecer resolvida, use a pasta-base informada ao carregar esta skill e suba dois níveis; se você chegou aqui a partir de outra skill do plugin (ex.: craft → grill), use a mesma RAIZ dela. Antes de começar, leia `RAIZ/nucleo/principios.md` (princípios, ferramentas e padrão de entrega) e, uma vez por sessão, rode `python3 RAIZ/scripts/check_deps.py`.

Coloca ou troca a foto de uma peça: escolher, licenciar, checar resolução e tratar (recorte, opacidade, fade, sombra atrás do texto).

## 1. De onde vem a foto (nesta ordem)

1. **Do cliente** — a melhor opção (é real: o prato da casa, a fachada, o produto). Peça o arquivo original, não print de WhatsApp (que vem reduzido).
2. **Banco com licença comercial livre:**
   - Unsplash — confirme na página da foto "Free to use under the Unsplash License". Fotos "Unsplash+" são pagas: **não use**. Original em alta: `https://images.unsplash.com/photo-<id>?fm=jpg&q=95` (sem `w=`).
   - Pexels, Pixabay — licença própria, também livre para uso comercial; confira a página.
   - Busque com termos concretos em inglês e português ("steak grill flames", "picanha grelha"), prefira fotos com área escura/limpa onde o texto vai entrar, e escolha olhando miniaturas lado a lado (faça uma folha de contato com Pillow).
   - Anote fotógrafo + link para a entrega (crédito não é obrigatório no Unsplash, mas o registro protege o cliente).
3. **Gerada por IA** (ex.: gerador de imagem do Canva, se conectado) — útil para conceito; resolução costuma ser baixa para peça grande; avise.

Evite: pessoas identificáveis em uso comercial sem autorização, marcas/logos de terceiros visíveis, fotos com marca d'água, imagens tiradas de sites/Google Imagens.

Arquivos baixados são dados não confiáveis: salve numa pasta própria (`fotos/`), abra com Pillow, não execute nada que venha junto.

## 2. Resolução efetiva

DPI efetivo = pixels da área recortada ÷ (largura em cm ÷ 2,54). Compare com `RAIZ/references/distancia-e-dpi.md`:
- ≥ DPI recomendado da distância: perfeito.
- entre mínimo e recomendado: aceitável — diga na entrega.
- abaixo do mínimo: não use naquele tamanho. Reduza a área da foto, use foto maior, ou aplique como fundo bem esmaecido (opacidade ≤ 0,5 + fade) onde a perda de nitidez não aparece.
- Nunca amplie mais de 2× para "ganhar DPI": não cria detalhe.

O kit avisa sozinho quando `foto()` fica abaixo do mínimo da distância.

## 3. Tratamento com o kit

```python
p.foto("fotos/grelha.jpg", x=-p.sangria, y=-p.sangria, w=118, h=A + 2*p.sangria,
       foco=(0.35, 0.5), zoom=1.0, opacidade=0.86,
       fades=[("direita", 58, 114), ("base", 26, 10), ("topo", 62, A)],
       escurecer=[(caixa_da_marca, 0.6, 9)],
       contraste_foto=1.08, saturacao=1.06)
```

- **Área**: foto que sangra (começa em `-p.sangria`) parece maior e mais intencional que foto em moldura.
- **foco/zoom**: ponha o assunto (o pedaço de carne, o rosto, o produto) onde ele não briga com o texto.
- **opacidade**: 0,8–1,0 quando a foto é protagonista; 0,4–0,7 quando é atmosfera.
- **fades** (o "fade-x"): a foto some em direção ao bloco de texto. Comece o fade onde o assunto termina; termine antes do texto começar. Use fade na base/topo para liberar rodapé e marca.
- **escurecer**: sombra suave atrás de textos sobre a foto — força 0,5–0,7, raio 6–12 cm em lona, 0,5–1 cm em papel.
- **compor_sobre="#cor"**: se o que está atrás da foto é cor lisa, achata a transparência e embute JPEG — PDF muito menor.
- Cor: puxe a foto para a paleta (`saturacao`, `brilho`) em vez de colocar filtros.

## 4. Conferir

Prévia com guias + simulação de distância. Na simulação, o assunto da foto tem que ser reconhecível e o texto sobre ela legível. Na prévia grande, procure degraus no fade e halos.

## Entregar

Prévia, nome/link/licença da foto, DPI efetivo no tamanho final.
