#!/usr/bin/env python3
"""Exemplo completo: banner de lona de promoção (foto à esquerda com fade-x, oferta à direita).

Ponto de partida — copie para a pasta de trabalho e troque textos, cores, foto e medidas.
  python3 exemplo_banner.py saida.pdf [foto.jpg]

Ordem que funciona: 1) fundo  2) medir tudo  3) foto (precisa saber onde ficam os textos para
escurecer atrás deles)  4) grafismos  5) textos  6) salvar (checagens).
"""
import os
import sys

sys.path.insert(0, os.environ.get("GRAFICA_KIT", os.path.dirname(os.path.abspath(__file__))))  # na cópia: PYTHONPATH=RAIZ/scripts
from grafica_kit import Caixa, Peca  # noqa: E402

SAIDA = sys.argv[1] if len(sys.argv) > 1 else "banner.pdf"
FOTO = sys.argv[2] if len(sys.argv) > 2 else None

# --- briefing (o que a entrevista do craft decidiu) ---
L, A = 200, 80                 # cm
DIST = 15                      # m — vista da calçada do outro lado da rua
FUNDO, CREME, AMBAR, VERMELHO, LARANJA = "#140E0B", "#F1E5D1", "#FFA833", "#C9341B", "#EC7A2C"
DISPLAY, APOIO, SERIFA = "BigShoulders-Bold", "InstrumentSans-Bold", "Gloock-Regular"

p = Peca(SAIDA, L, A, material="lona", distancia_m=DIST, titulo="Banner promoção — exemplo")
u = p.area_util                # área segura (dentro da margem de segurança)

# 1) fundo e luz
p.fundo(FUNDO)
p.gradiente_radial(130, -15, 120, ["#4A1609", "#2C110A", "#1B110C", FUNDO], [0, 0.38, 0.72, 1])

# 2) medidas da marca (canto superior esquerdo) — antes da foto, para escurecer atrás dela
seg_cap, marca_cap = 1.9, 10.0
y_marca = u.y1 - seg_cap - 2.6 - marca_cap
caixa_marca = Caixa(u.x0, y_marca - 3.5, u.x0 + p.medir("Tição", SERIFA, cap=marca_cap).w, u.y1)

# 3) foto com opacidade e fade-x (some antes da oferta), fade na base (some antes do rodapé)
if FOTO:
    p.foto(FOTO, x=-p.sangria, y=-p.sangria, w=118, h=A + 2 * p.sangria, foco=(0.35, 0.5),
           opacidade=0.86, fades=[("direita", 58, 114), ("base", 26, 10), ("topo", 62, A)],
           escurecer=[(caixa_marca, 0.6, 9)])

# 4) bloco da oferta, alinhado à direita da área útil.
#    Regra de distância (15 m): o que precisa ser lido da rua tem maiúscula ≥ 4,2 cm (letra mínima);
#    o que só importa para quem se aproxima vai como papel="detalhe".
titulo, cap_tit = "RODÍZIO DO ALMOÇO", 6.3
x_bloco = u.x1 - p.medir(titulo, DISPLAY, cap=cap_tit, tracking=0.6).w
tag_cap, pad = 4.2, 1.3
tag_w = p.medir("PROMOÇÃO", DISPLAY, cap=tag_cap, tracking=0.7).w + 2 * pad * 1.4
p.retangulo(x_bloco, u.y1 - tag_cap - 2 * pad, tag_w, tag_cap + 2 * pad, preenchimento=VERMELHO,
            nome="etiqueta", papel="conteudo")
p.texto("PROMOÇÃO", DISPLAY, x_bloco + pad * 1.4, u.y1 - tag_cap - pad, cap=tag_cap, cor_texto=CREME,
        tracking=0.7, nome="promo", sobre="etiqueta")
y_tit = u.y1 - tag_cap - 2 * pad - 2.4 - cap_tit
p.texto(titulo, DISPLAY, x_bloco, y_tit, cap=cap_tit, cor_texto=CREME, tracking=0.6, nome="titulo")

# preço: o maior tamanho que cabe na largura do bloco e na altura que sobrou, centrado nesse vão
piso, teto = u.y0 + 2.4 + 3.0, y_tit - 3.2          # acima do horário, abaixo do título
med = p.preco("99,99", DISPLAY, x_bloco, piso, largura_max=u.x1 - x_bloco, altura_max=teto - piso, desenhar=False)
base_preco = piso + (teto - piso - med["cap"]) / 2
pr = p.preco("99,99", DISPLAY, x_bloco, base_preco, cap=med["cap"], cor_texto=AMBAR)
p.texto("por pessoa", "InstrumentSerif-Italic", pr["centavos"].x0, base_preco + 0.6, cap=3.0, cor_texto=CREME,
        nome="por-pessoa", papel="detalhe")
p.texto("SEG A SEX · 11H30 ÀS 15H", APOIO, x_bloco, u.y0, cap=2.4, cor_texto=CREME, tracking=0.35,
        nome="horario", papel="detalhe")

# 5) marca
ch = p.texto("CHURRASCARIA", "BigShoulders-Regular", u.x0, u.y1, cap=seg_cap, cor_texto=LARANJA, tracking=1.0,
             ancora="topo", nome="segmento", papel="detalhe")
p.texto("Tição", SERIFA, u.x0, y_marca, cap=marca_cap, cor_texto=CREME, nome="marca")
p.texto("rodízio de carnes nobres na brasa", "InstrumentSerif-Italic", u.x0, y_marca - 6.5, cap=2.4,
        cor_texto=CREME, nome="tagline", papel="detalhe")

# 6) gravar + checagens (sobreposição, margem, letra mínima para 15 m, DPI da foto)
p.salvar()
