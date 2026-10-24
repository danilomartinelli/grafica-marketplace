"""grafica_kit — monta peças gráficas impressas como PDF vetorial no tamanho final.

Uso típico (veja scripts/exemplo_banner.py):

    import sys; sys.path.insert(0, "<pasta da skill>/scripts")
    from grafica_kit import Peca
    p = Peca("banner.pdf", largura=200, altura=80, material="lona", distancia_m=15)
    p.fundo("#130D0A")
    p.texto("RODÍZIO", "Anton-Regular", x=190, y=60, cap=8, cor_texto="#F1E5D1", alinhar="direita", nome="titulo")
    p.preco("99,99", "Anton-Regular", x=190, y_base=20, cap=30, cor_texto="#FFA833", alinhar="direita")
    p.salvar()   # grava o PDF, roda as checagens e grava banner.spec.json

Recursos principais
- Peca(arquivo, largura, altura, material=, distancia_m=, cores="rgb"|"cmyk", marcas_corte=)
- fundo, gradiente_linear/radial, retangulo, circulo, linha, poligono
- texto (alinhamento óptico pela tinta; texto gigante vira curvas + camada pesquisável), paragrafo
- preco("39,90", ..., de="59,90") — preço de varejo, opcionalmente "de R$ X por"
- foto(cover, foco, zoom, opacidade, fades, escurecer) · imagem (logo) · qrcode
- cor: contraste(), ajustar_contraste(), relatorio_cores(), simular_cor()
- salvar(): PDF + .spec.json + checagens (sobreposição, margem, letra mínima, contraste, DPI)

Convenções
- Unidades em cm. Origem (0, 0) no canto inferior esquerdo da ÁREA FINAL (linha de corte).
  A sangria fica fora dela: x < 0, x > largura, y < 0, y > altura.
- `cap` = altura da letra maiúscula em cm (é o que importa para leitura à distância).
  Para peças de mão dá para usar `pt=` (tamanho de fonte em pontos) no lugar.
- Todo texto é medido pela tinta real dos glifos (não pela caixa da fonte), então
  alinhamentos e checagens de sobreposição batem com o que sai impresso.
- `nome=` registra o elemento para as checagens. `papel=` muda como ele é checado:
  "texto" (padrão), "detalhe" (texto pequeno de propósito, só para quem chega perto),
  "conteudo" (logo, QR, selo — precisa respeitar a margem de segurança),
  "decorativo" (pode sangrar e ficar sob textos).
"""
from __future__ import annotations

import glob
import json
import math
import os
import sys
import tempfile
from dataclasses import dataclass, field

import numpy as np
from fontTools.pens.basePen import BasePen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageEnhance, ImageOps
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr as rl_qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import CMYKColor, Color, HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLFont
from reportlab.pdfgen import canvas as rl_canvas

# Windows: saída para o terminal/pipe em UTF-8 (✓ ✗ × ã) sem quebrar no cp1252
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

CM = 72 / 2.54
FONTE_PADRAO = "WorkSans-Regular"
# Acima disso o texto vira curvas (+ camada invisível pesquisável): o poppler (pdftoppm e
# visualizadores baseados nele) deixa de desenhar glifos com mais de ~1440 pt — o preço
# gigante some da prévia/JPEG mesmo estando no PDF. Curvas são seguras em qualquer RIP.
LIMITE_TEXTO_VIVO_PT = 1200
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIRS = [
    os.path.join(SKILL_DIR, "assets", "fonts"),
    "/mnt/skills/examples/canvas-design/canvas-fonts",
    os.path.expanduser("~/.fonts"),
    os.path.expanduser("~/.local/share/fonts"),
    "/usr/share/fonts",
]

# ---------------------------------------------------------------------------
# Distância de leitura → letra e resolução
# ---------------------------------------------------------------------------
# Regra de sinalização: 1 cm de letra maiúscula é lido a ~3,6 m (limite) e tem
# impacto (leitura sem esforço, de passagem) até ~1,2 m. Ou seja:
#   letra mínima  ≈ distância × 0,28 cm/m
#   letra impacto ≈ distância × 0,83 cm/m
LETRA_MIN_CM_POR_M = 0.28
LETRA_IMPACTO_CM_POR_M = 0.83

FAIXAS_DISTANCIA = [
    # (até m, nome, dpi recomendado, dpi mínimo aceitável para fotos)
    (1.0, "perto (na mão)", 300, 240),
    (3.0, "média (balcão, parede, vitrine)", 200, 120),
    (10.0, "longe (calçada, fachada baixa)", 150, 72),
    (30.0, "muito longe (rua, fachada alta)", 100, 45),
    (1e9, "outdoor / empena", 50, 20),
]

MATERIAIS = {
    # material: (sangria cm, segurança cm, observação)
    "papel": (0.3, 0.5, "papel/couchê: sangria 3 mm, textos a 5 mm do corte"),
    "cartao": (0.3, 0.4, "cartão de visita: sangria 3 mm, textos a 4 mm do corte"),
    "adesivo": (0.2, 0.3, "vinil adesivo: sangria 2 mm, segurança 3 mm"),
    "lona": (1.0, 4.0, "lona com ilhós/bastão: confirme sangria com a gráfica; nada a menos de 4 cm da borda"),
    "faixa": (1.0, 4.0, "faixa de lona: idem lona"),
    "pvc": (0.3, 1.0, "placa PVC/ACM: sangria 3 mm, segurança 1 cm (furos)"),
    "outdoor": (5.0, 10.0, "outdoor/empena: sangria e área útil definidas pela exibidora"),
}


ICC_CMYK_CANDIDATOS = [
    os.environ.get("GRAFICA_ICC", ""),
    "/usr/share/texlive/texmf-dist/tex/generic/colorprofiles/FOGRA39L_coated.icc",
    "/usr/share/color/icc/ISOcoated_v2_eci.icc",
    "/usr/share/color/icc/ghostscript/default_cmyk.icc",
    "/usr/share/ghostscript/iccprofiles/default_cmyk.icc",
    # macOS e Windows trazem perfis CMYK genéricos (não são FOGRA39, mas servem quando a gráfica não manda o dela)
    "/System/Library/ColorSync/Profiles/Generic CMYK Profile.icc",
    os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "spool", "drivers", "color", "RSWOP.icm"),
]


def perfil_cmyk():
    """Caminho de um perfil ICC CMYK, nesta ordem: variável GRAFICA_ICC; um .icc/.icm na pasta de trabalho
    (ou em marca/), que é o jeito mais simples de usar o perfil mandado pela gráfica; FOGRA39 ou outro
    perfil CMYK do sistema."""
    if os.environ.get("GRAFICA_ICC") and os.path.exists(os.environ["GRAFICA_ICC"]):
        return os.environ["GRAFICA_ICC"]
    for pasta in (os.getcwd(), os.path.join(os.getcwd(), "marca")):
        locais = sorted(glob.glob(os.path.join(pasta, "*.ic[cm]")) + glob.glob(os.path.join(pasta, "*.IC[CM]")))
        if locais:
            return locais[0]
    for p in ICC_CMYK_CANDIDATOS:
        if p and os.path.exists(p):
            return p
    pastas = ["/usr/share", "/Library/ColorSync/Profiles", os.path.expanduser("~/Library/ColorSync/Profiles"),
              os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "spool", "drivers", "color")]
    for pasta in pastas:
        for p in glob.glob(os.path.join(pasta, "**", "*.ic[cm]"), recursive=True):
            n = os.path.basename(p).lower()
            if any(k in n for k in ("fogra", "coated", "cmyk", "swop", "gracol")):
                return p
    return None


def letra_minima_cm(distancia_m: float) -> float:
    return max(0.15, distancia_m * LETRA_MIN_CM_POR_M)


def letra_impacto_cm(distancia_m: float) -> float:
    return max(0.3, distancia_m * LETRA_IMPACTO_CM_POR_M)


def faixa_distancia(distancia_m: float):
    for ate, nome, dpi, dpi_min in FAIXAS_DISTANCIA:
        if distancia_m <= ate:
            return {"nome": nome, "dpi": dpi, "dpi_min": dpi_min}
    raise AssertionError


def distancia_legivel_m(cap_cm: float) -> tuple[float, float]:
    """(distância de impacto, distância máxima legível) para uma letra de `cap_cm`."""
    return cap_cm / LETRA_IMPACTO_CM_POR_M, cap_cm / LETRA_MIN_CM_POR_M


# ---------------------------------------------------------------------------
# Cores
# ---------------------------------------------------------------------------
def cor(c):
    """'#RRGGBB', (r,g,b) 0-255, 'cmyk(c,m,y,k)' em % ou um objeto Color."""
    if isinstance(c, Color):
        return c
    if isinstance(c, str):
        s = c.strip().lower()
        if s.startswith("cmyk(") and s.endswith(")"):
            vals = [float(v) / 100 for v in s[5:-1].split(",")]
            return CMYKColor(*vals)
        return HexColor(c)
    if isinstance(c, (tuple, list)) and len(c) == 3:
        return Color(*(v / 255 for v in c))
    raise ValueError(f"cor inválida: {c!r}")


def _rgb01(c):
    c = cor(c)
    if isinstance(c, CMYKColor):
        k = c.black
        return ((1 - c.cyan) * (1 - k), (1 - c.magenta) * (1 - k), (1 - c.yellow) * (1 - k))
    return (c.red, c.green, c.blue)


def contraste(c1, c2) -> float:
    """Razão de contraste WCAG entre duas cores (1 a 21). Rua: ≥ 7 ideal; ≥ 4,5 mínimo."""

    def lum(c):
        r = []
        for v in _rgb01(c):
            r.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
        return 0.2126 * r[0] + 0.7152 * r[1] + 0.0722 * r[2]

    a, b = sorted([lum(c1), lum(c2)], reverse=True)
    return (a + 0.05) / (b + 0.05)


def _hex(rgb01):
    return "#%02X%02X%02X" % tuple(int(round(max(0, min(1, v)) * 255)) for v in rgb01)


def ajustar_contraste(c, fundo, alvo=4.5):
    """Escurece ou clareia `c` mantendo o tom (matiz e saturação) até atingir `alvo`:1 contra `fundo`.

    É o jeito de usar a cor da marca em texto sem trocá-la por outra: ex. laranja da marca
    sobre creme vira um laranja-queimado do mesmo tom. Retorna '#RRGGBB' (a melhor possível
    se o alvo for inalcançável — confira com contraste())."""
    import colorsys

    r, g, b = _rgb01(c)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if contraste(c, fundo) >= alvo:
        return _hex((r, g, b))
    escuro = sum(_rgb01(fundo)) / 3 > 0.5  # fundo claro → texto mais escuro
    lo, hi = (0.0, l) if escuro else (l, 1.0)
    melhor = _hex((r, g, b))
    for _ in range(30):
        mid = (lo + hi) / 2
        cand = _hex(colorsys.hls_to_rgb(h, mid, s))
        if contraste(cand, fundo) >= alvo:
            melhor = cand
            lo, hi = (mid, hi) if escuro else (lo, mid)
        else:
            lo, hi = (lo, mid) if escuro else (mid, hi)
    if contraste(melhor, fundo) < alvo:
        melhor = _hex(colorsys.hls_to_rgb(h, 0.0 if escuro else 1.0, s))
    return melhor


# Machado, Oliveira & Fernandes (2009), severidade 1.0, aplicadas em RGB linear
_CVD = {
    "deuteranopia": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    "protanopia": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    "tritanopia": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}


def _lin(v):
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def _srgb(v):
    v = max(0.0, min(1.0, v))
    return v * 12.92 if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055


def simular_cor(c, tipo):
    """Como uma pessoa com deuteranopia/protanopia/tritanopia vê a cor (ou 'cinza')."""
    r, g, b = _rgb01(c)
    if tipo == "cinza":
        y = 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)
        return _hex((_srgb(y),) * 3)
    m = _CVD[tipo]
    lr, lg, lb = _lin(r), _lin(g), _lin(b)
    return _hex(tuple(_srgb(m[i][0] * lr + m[i][1] * lg + m[i][2] * lb) for i in range(3)))


def relatorio_cores(cores: dict, imprimir=True):
    """Matriz de contraste entre as cores de uma paleta {nome: cor}, com o pior caso entre
    visão típica, deuteranopia, protanopia e tritanopia. Legenda: ≥7 rua/N1 · ≥4,5 texto ·
    ≥3 só letras grandes/grafismos · <3 não use texto."""
    nomes = list(cores)
    linhas = ["Contraste (pior caso com daltonismo entre parênteses):"]
    pares = []
    for i in range(len(nomes)):
        for j in range(i + 1, len(nomes)):
            a, b = cores[nomes[i]], cores[nomes[j]]
            r = contraste(a, b)
            pior = min([r] + [contraste(simular_cor(a, t), simular_cor(b, t)) for t in _CVD])
            uso = "rua/N1" if pior >= 7 else "texto" if pior >= 4.5 else "só grande" if pior >= 3 else "não use p/ texto"
            pares.append((nomes[i], nomes[j], r, pior, uso))
    for a, b, r, pior, uso in sorted(pares, key=lambda q: -q[3]):
        linhas.append(f"  {a:>14} × {b:<14} {r:5.1f}:1 ({pior:4.1f}:1)  {uso}")
    if imprimir:
        print("\n".join(linhas))
    return pares


# ---------------------------------------------------------------------------
# Fontes
# ---------------------------------------------------------------------------
_FONT_INDEX: dict[str, str] | None = None
_FT: dict[str, TTFont] = {}
_REGISTERED: set[str] = set()


def _index_fonts():
    global _FONT_INDEX
    if _FONT_INDEX is None:
        _FONT_INDEX = {}
        for d in FONT_DIRS:
            for p in glob.glob(os.path.join(d, "**", "*.[ot]tf"), recursive=True):
                stem = os.path.splitext(os.path.basename(p))[0]
                _FONT_INDEX.setdefault(stem, p)
    return _FONT_INDEX


def fontes_disponiveis() -> list[str]:
    return sorted(_index_fonts())


def registrar_fonte(caminho: str, nome: str | None = None) -> str:
    """Registra uma fonte .ttf extra (ex.: a fonte da marca do cliente)."""
    nome = nome or os.path.splitext(os.path.basename(caminho))[0]
    _index_fonts()[nome] = caminho
    return nome


def _font(nome: str) -> TTFont:
    idx = _index_fonts()
    if nome not in idx:
        parecidas = [f for f in idx if nome.lower().split("-")[0] in f.lower()][:8]
        raise ValueError(f"fonte '{nome}' não encontrada. Parecidas: {parecidas or fontes_disponiveis()[:20]}")
    if nome not in _FT:
        t = TTFont(idx[nome])
        if "fvar" in t:
            raise ValueError(f"'{nome}' é fonte variável; gere uma instância estática (fontTools.varLib.instancer)")
        _FT[nome] = t
    if nome not in _REGISTERED:
        pdfmetrics.registerFont(RLFont(nome, idx[nome]))
        _REGISTERED.add(nome)
    return _FT[nome]


def _glyph(nome, ch):
    t = _font(nome)
    cmap = t.getBestCmap()
    if ord(ch) not in cmap:
        raise ValueError(f"a fonte '{nome}' não tem o caractere {ch!r} — troque de fonte ou de texto")
    g = cmap[ord(ch)]
    gs = t.getGlyphSet()
    pen = BoundsPen(gs)
    gs[g].draw(pen)
    upm = t["head"].unitsPerEm
    adv = t["hmtx"][g][0] / upm
    b = pen.bounds
    return (None if b is None else tuple(v / upm for v in b)), adv


_OTICO: dict = {}


def _tinta_acima_da_base(nome, ch):
    """(xmin, xmax) dos pontos do glifo acima da linha de base, em em. Alinha pela haste:
    ignora o gancho do 'j', a cauda do 'Q'/',' etc. None se o glifo não tem nada acima."""
    k = (nome, ch)
    if k not in _OTICO:
        t = _font(nome)
        g = t.getBestCmap()[ord(ch)]
        gs = t.getGlyphSet()
        rp = RecordingPen()
        gs[g].draw(rp)
        upm = t["head"].unitsPerEm
        xs = [pt[0] for _, pts in rp.value for pt in pts if pt[1] >= 0]
        _OTICO[k] = (min(xs) / upm, max(xs) / upm) if xs else None
    return _OTICO[k]


class _CanvasPen(BasePen):
    """Desenha contornos de glifo num caminho do reportlab (para texto em curvas)."""

    def __init__(self, glyphset, path, escala, dx, dy):
        super().__init__(glyphset)
        self.p, self.s, self.dx, self.dy = path, escala, dx, dy

    def _t(self, pt):
        return self.dx + pt[0] * self.s, self.dy + pt[1] * self.s

    def _moveTo(self, pt):
        self.p.moveTo(*self._t(pt))

    def _lineTo(self, pt):
        self.p.lineTo(*self._t(pt))

    def _curveToOne(self, p1, p2, p3):
        self.p.curveTo(*self._t(p1), *self._t(p2), *self._t(p3))

    def _closePath(self):
        self.p.close()


def cap_ratio(fonte: str) -> float:
    b, _ = _glyph(fonte, "H")
    return b[3]


@dataclass
class Caixa:
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def w(self):
        return self.x1 - self.x0

    @property
    def h(self):
        return self.y1 - self.y0

    @property
    def cx(self):
        return (self.x0 + self.x1) / 2

    @property
    def cy(self):
        return (self.y0 + self.y1) / 2

    def expandir(self, m):
        return Caixa(self.x0 - m, self.y0 - m, self.x1 + m, self.y1 + m)

    def tupla(self):
        return (self.x0, self.y0, self.x1, self.y1)

    def cruza(self, o: "Caixa", folga=0.0):
        return self.x0 < o.x1 + folga and o.x0 < self.x1 + folga and self.y0 < o.y1 + folga and o.y0 < self.y1 + folga


def medir(texto: str, fonte: str, tamanho_cm: float, tracking: float = 0.0):
    """Caixa da tinta relativa à origem do texto (baseline), em cm, e o avanço total."""
    x = 0.0
    xmin = ymin = math.inf
    xmax = ymax = -math.inf
    for i, ch in enumerate(texto):
        b, adv = _glyph(fonte, ch)
        if b is not None:
            xmin = min(xmin, x + b[0] * tamanho_cm)
            xmax = max(xmax, x + b[2] * tamanho_cm)
            ymin = min(ymin, b[1] * tamanho_cm)
            ymax = max(ymax, b[3] * tamanho_cm)
        x += adv * tamanho_cm + (tracking if i < len(texto) - 1 else 0)
    if xmin is math.inf:
        xmin = xmax = ymin = ymax = 0.0
    return Caixa(xmin, ymin, xmax, ymax), x


# ---------------------------------------------------------------------------
# A peça
# ---------------------------------------------------------------------------
@dataclass
class Elemento:
    nome: str
    papel: str
    caixa: Caixa
    sobre: tuple = ()
    cap_cm: float | None = None
    info: dict = field(default_factory=dict)


class Peca:
    def __init__(
        self,
        arquivo: str,
        largura: float,
        altura: float,
        material: str = "papel",
        distancia_m: float = 1.0,
        sangria: float | None = None,
        seguranca: float | None = None,
        marcas_corte: bool = False,
        titulo: str = "",
        autor: str = "",
        cores: str = "rgb",
    ):
        if material not in MATERIAIS:
            raise ValueError(f"material deve ser um de {list(MATERIAIS)}")
        sg, seg, nota = MATERIAIS[material]
        self.arquivo = arquivo
        self.W, self.H = float(largura), float(altura)
        self.material = material
        self.nota_material = nota
        self.distancia_m = float(distancia_m)
        self.sangria = sg if sangria is None else float(sangria)
        self.seguranca = seg if seguranca is None else float(seguranca)
        self.marcas_corte = marcas_corte
        self.faixa = faixa_distancia(self.distancia_m)
        self.elementos: list[Elemento] = []
        self.avisos: list[str] = []
        self.fotos: list[dict] = []
        self.pagina = 1
        self._tmp = tempfile.mkdtemp(prefix="grafica_")
        self.modo_cor = cores.lower()
        self._ultimo_fundo = "#FFFFFF"
        self._xf_vetor = self._xf_foto = None
        self.icc = None
        if self.modo_cor == "cmyk":
            from PIL import ImageCms

            self.icc = perfil_cmyk()
            if not self.icc:
                raise RuntimeError("modo CMYK precisa de um perfil ICC CMYK: defina GRAFICA_ICC=/caminho/perfil.icc "
                                   "(peça o da gráfica, ou use FOGRA39/ISO Coated v2)")
            srgb, alvo = ImageCms.createProfile("sRGB"), ImageCms.getOpenProfile(self.icc)
            self._xf_vetor = ImageCms.buildTransform(srgb, alvo, "RGB", "CMYK", renderingIntent=1)  # colorimétrico relativo
            self._xf_foto = ImageCms.buildTransform(srgb, alvo, "RGB", "CMYK", renderingIntent=0)   # perceptual
            self._cache_cmyk = {}
        elif self.modo_cor != "rgb":
            raise ValueError("cores deve ser 'rgb' ou 'cmyk'")

        self.margem_marcas = 1.0 if marcas_corte else 0.0  # espaço para as marcas além da sangria
        off = self.sangria + self.margem_marcas
        self._off = off
        pw, ph = self.W + 2 * off, self.H + 2 * off
        _font(FONTE_PADRAO)  # registra antes: o canvas abre com ela em vez de Helvetica (não incorporada)
        self.c = rl_canvas.Canvas(arquivo, pagesize=(pw * CM, ph * CM), initialFontName=FONTE_PADRAO)
        if titulo:
            self.c.setTitle(titulo)
        if autor:
            self.c.setAuthor(autor)
        self.c.setCreator("grafica_kit")
        trim = (off * CM, off * CM, (off + self.W) * CM, (off + self.H) * CM)
        bleed = ((off - self.sangria) * CM, (off - self.sangria) * CM, (off + self.W + self.sangria) * CM, (off + self.H + self.sangria) * CM)
        self.c.setTrimBox(trim)
        self.c.setBleedBox(bleed)
        self._iniciar_pagina()

    # ---- infraestrutura ----
    def _cor(self, c):
        """Cor no espaço da peça: em modo CMYK converte RGB/hex pelo perfil ICC (cores CMYK passam direto)."""
        k = cor(c)
        if self.modo_cor != "cmyk" or isinstance(k, CMYKColor):
            return k
        chave = _hex(_rgb01(k))
        if chave not in self._cache_cmyk:
            from PIL import ImageCms

            px = ImageCms.applyTransform(Image.new("RGB", (1, 1), tuple(int(round(v * 255)) for v in _rgb01(k))), self._xf_vetor).getpixel((0, 0))
            self._cache_cmyk[chave] = CMYKColor(*(v / 255 for v in px))
        return self._cache_cmyk[chave]

    def _iniciar_pagina(self):
        self.c.translate(self._off * CM, self._off * CM)
        # tudo que for desenhado fica recortado na área de sangria (foto grande não cobre as marcas de corte)
        self.c.saveState()
        a = self.area_sangria
        p = self.c.beginPath()
        p.rect(a.x0 * CM, a.y0 * CM, a.w * CM, a.h * CM)
        self.c.clipPath(p, stroke=0, fill=0)

    def nova_pagina(self):
        """Fecha a página atual (ex.: frente) e começa outra igual (ex.: verso)."""
        self._finalizar_pagina()
        self.c.showPage()
        self.pagina += 1
        self._iniciar_pagina()

    def _finalizar_pagina(self):
        self.c.restoreState()  # fecha o recorte da sangria aberto em _iniciar_pagina
        if self.marcas_corte:
            self._desenhar_marcas()

    def _desenhar_marcas(self):
        c = self.c
        c.saveState()
        c.setStrokeColor(CMYKColor(1, 1, 1, 1))  # cor de registro
        c.setLineWidth(0.25)
        ini = self.sangria + 0.1
        fim = ini + 0.6
        for x in (0, self.W):
            for y in (0, self.H):
                sx = -1 if x == 0 else 1
                sy = -1 if y == 0 else 1
                c.line(x * CM + sx * ini * CM, y * CM, x * CM + sx * fim * CM, y * CM)
                c.line(x * CM, y * CM + sy * ini * CM, x * CM, y * CM + sy * fim * CM)
        c.restoreState()

    def _reg(self, nome, papel, caixa, sobre=(), cap=None, **info):
        if nome is None:
            return
        if isinstance(sobre, str):
            sobre = (sobre,)
        self.elementos.append(Elemento(f"p{self.pagina}:{nome}", papel, caixa, tuple(f"p{self.pagina}:{s}" for s in sobre), cap, info))

    def registrar(self, nome, caixa: Caixa | tuple, papel="conteudo", sobre=()):
        """Registra manualmente uma área (ex.: um desenho feito direto no canvas)."""
        if isinstance(caixa, tuple):
            caixa = Caixa(*caixa)
        self._reg(nome, papel, caixa, sobre)

    @property
    def area_util(self) -> Caixa:
        s = self.seguranca
        return Caixa(s, s, self.W - s, self.H - s)

    @property
    def area_sangria(self) -> Caixa:
        b = self.sangria
        return Caixa(-b, -b, self.W + b, self.H + b)

    # ---- formas e fundos ----
    def fundo(self, c):
        a = self.area_sangria
        self._ultimo_fundo = c
        self.c.setFillColor(self._cor(c))
        self.c.rect(a.x0 * CM, a.y0 * CM, a.w * CM, a.h * CM, stroke=0, fill=1)

    def _clip(self, area: Caixa | None):
        a = area or self.area_sangria
        p = self.c.beginPath()
        p.rect(a.x0 * CM, a.y0 * CM, a.w * CM, a.h * CM)
        self.c.clipPath(p, stroke=0, fill=0)

    def gradiente_linear(self, x0, y0, x1, y1, cores, posicoes=None, area: Caixa | None = None):
        self.c.saveState()
        self._clip(area)
        self.c.linearGradient(x0 * CM, y0 * CM, x1 * CM, y1 * CM, [self._cor(k) for k in cores], posicoes, extend=True)
        self.c.restoreState()

    def gradiente_radial(self, cx, cy, r, cores, posicoes=None, area: Caixa | None = None):
        self.c.saveState()
        self._clip(area)
        self.c.radialGradient(cx * CM, cy * CM, r * CM, [self._cor(k) for k in cores], posicoes, extend=True)
        self.c.restoreState()

    def retangulo(self, x, y, w, h, preenchimento=None, contorno=None, espessura=0.1, raio=0.0, opacidade=1.0, nome=None, papel="decorativo", sobre=()):
        c = self.c
        c.saveState()
        if opacidade < 1:
            c.setFillAlpha(opacidade)
            c.setStrokeAlpha(opacidade)
        if preenchimento is not None:
            c.setFillColor(self._cor(preenchimento))
        if contorno is not None:
            c.setStrokeColor(self._cor(contorno))
            c.setLineWidth(espessura * CM)
        args = (x * CM, y * CM, w * CM, h * CM)
        fill, stroke = int(preenchimento is not None), int(contorno is not None)
        if raio > 0:
            c.roundRect(*args, raio * CM, stroke=stroke, fill=fill)
        else:
            c.rect(*args, stroke=stroke, fill=fill)
        c.restoreState()
        cx = Caixa(x, y, x + w, y + h)
        self._reg(nome, papel, cx, sobre)
        return cx

    def circulo(self, cx, cy, r, preenchimento=None, contorno=None, espessura=0.1, opacidade=1.0, nome=None, papel="decorativo"):
        c = self.c
        c.saveState()
        if opacidade < 1:
            c.setFillAlpha(opacidade)
            c.setStrokeAlpha(opacidade)
        if preenchimento is not None:
            c.setFillColor(self._cor(preenchimento))
        if contorno is not None:
            c.setStrokeColor(self._cor(contorno))
            c.setLineWidth(espessura * CM)
        c.circle(cx * CM, cy * CM, r * CM, stroke=int(contorno is not None), fill=int(preenchimento is not None))
        c.restoreState()
        b = Caixa(cx - r, cy - r, cx + r, cy + r)
        self._reg(nome, papel, b)
        return b

    def linha(self, x0, y0, x1, y1, cor_linha="#000000", espessura=0.1, opacidade=1.0):
        c = self.c
        c.saveState()
        if opacidade < 1:
            c.setStrokeAlpha(opacidade)
        c.setStrokeColor(self._cor(cor_linha))
        c.setLineWidth(espessura * CM)
        c.line(x0 * CM, y0 * CM, x1 * CM, y1 * CM)
        c.restoreState()

    def poligono(self, pontos, preenchimento, opacidade=1.0, nome=None, papel="decorativo"):
        c = self.c
        c.saveState()
        if opacidade < 1:
            c.setFillAlpha(opacidade)
        c.setFillColor(self._cor(preenchimento))
        p = c.beginPath()
        p.moveTo(pontos[0][0] * CM, pontos[0][1] * CM)
        for x, y in pontos[1:]:
            p.lineTo(x * CM, y * CM)
        p.close()
        c.drawPath(p, stroke=0, fill=1)
        c.restoreState()
        xs, ys = [q[0] for q in pontos], [q[1] for q in pontos]
        b = Caixa(min(xs), min(ys), max(xs), max(ys))
        self._reg(nome, papel, b)
        return b

    # ---- texto ----
    def tamanho(self, fonte, cap=None, pt=None):
        """Converte cap (cm) ou pt no tamanho de fonte em cm."""
        if cap is not None:
            return cap / cap_ratio(fonte)
        if pt is not None:
            return pt / CM
        raise ValueError("informe cap= (cm) ou pt=")

    def medir(self, texto, fonte, cap=None, pt=None, tracking=0.0) -> Caixa:
        cx, _ = medir(texto, fonte, self.tamanho(fonte, cap, pt), tracking)
        return cx

    def cap_para_largura(self, texto, fonte, largura, tracking=0.0, cap_max=None):
        """Maior cap (cm) que faz o texto caber em `largura` cm."""
        ref = 10.0
        b, _ = medir(texto, fonte, self.tamanho(fonte, cap=ref), tracking)
        cap = ref * largura / b.w
        # tracking não escala: refina duas vezes
        for _ in range(2):
            b, _ = medir(texto, fonte, self.tamanho(fonte, cap=cap), tracking)
            cap *= largura / b.w
        return min(cap, cap_max) if cap_max else cap

    def texto(self, texto, fonte, x, y, cap=None, pt=None, cor_texto="#000000", tracking=0.0, alinhar="esquerda",
              ancora="base", nome=None, papel="texto", sobre=(), opacidade=1.0, fundo=None, registrar=True,
              em_curvas=None):
        """Desenha uma linha de texto.

        alinhar: esquerda | centro | direita — pela tinta real acima da linha de base (alinhamento
                 óptico: o 'R' começa exatamente em x; o gancho do 'j' e caudas podem passar um pouco).
        ancora:  base (y é a linha de base) | topo (y é o topo das maiúsculas) | meio (y é o meio das maiúsculas).
        fundo:   cor de fundo atrás do texto, para checar contraste (opcional).
        em_curvas: None = automático (acima de LIMITE_TEXTO_VIVO_PT vira curvas + texto invisível).
        """
        size = self.tamanho(fonte, cap, pt)
        _font(fonte)
        ink, adv = medir(texto, fonte, size, tracking)
        caph = cap_ratio(fonte) * size
        # posições de cada caractere (para alinhamento óptico e curvas)
        pos, xx = [], 0.0
        for i, ch in enumerate(texto):
            pos.append(xx)
            xx += _glyph(fonte, ch)[1] * size + (tracking if i < len(texto) - 1 else 0)
        idx = [i for i, ch in enumerate(texto) if not ch.isspace()]
        if alinhar == "esquerda":
            o = _tinta_acima_da_base(fonte, texto[idx[0]]) if idx else None
            ox = x - (pos[idx[0]] + o[0] * size if o else ink.x0)
        elif alinhar == "direita":
            o = _tinta_acima_da_base(fonte, texto[idx[-1]]) if idx else None
            ox = x - (pos[idx[-1]] + o[1] * size if o else ink.x1)
        elif alinhar == "centro":
            ox = x - (ink.x0 + ink.x1) / 2
        else:
            raise ValueError("alinhar: esquerda|centro|direita")
        if ancora == "base":
            oy = y
        elif ancora == "topo":
            oy = y - caph
        elif ancora == "meio":
            oy = y - caph / 2
        else:
            raise ValueError("ancora: base|topo|meio")
        curvas = (size * CM > LIMITE_TEXTO_VIVO_PT) if em_curvas is None else em_curvas
        self.c.saveState()
        if opacidade < 1:
            self.c.setFillAlpha(opacidade)
        if curvas:
            tf = _font(fonte)
            gs = tf.getGlyphSet()
            cmap = tf.getBestCmap()
            esc = size * CM / tf["head"].unitsPerEm
            path = self.c.beginPath()
            for ch, px in zip(texto, pos):
                if ch.isspace():
                    continue
                gs[cmap[ord(ch)]].draw(_CanvasPen(gs, path, esc, (ox + px) * CM, oy * CM))
            self.c.setFillColor(self._cor(cor_texto))
            self.c.drawPath(path, stroke=0, fill=1, fillMode=1)  # non-zero, como as fontes TrueType
        t = self.c.beginText()
        t.setTextOrigin(ox * CM, oy * CM)
        t.setFont(fonte, size * CM)
        t.setCharSpace(tracking * CM)
        t.setFillColor(self._cor(cor_texto))
        if curvas:
            t.setTextRenderMode(3)  # invisível: o texto continua pesquisável/copiável no PDF
        t.textLine(texto)
        self.c.drawText(t)
        self.c.restoreState()
        box = Caixa(ox + ink.x0, oy + ink.y0, ox + ink.x1, oy + ink.y1)
        if fundo is not None:
            r = contraste(cor_texto, fundo)
            minimo = 3.0 if caph >= 2 else 4.5
            if r < minimo:
                self.avisos.append(f"contraste baixo ({r:.1f}:1) em '{texto[:30]}' — mínimo {minimo}:1")
        if registrar:
            self._reg(nome or texto[:24], papel, box, sobre, cap=caph, texto=texto, fonte=fonte)
        return box

    def paragrafo(self, texto, fonte, x, y_topo, largura, cap=None, pt=None, cor_texto="#000000", entrelinha=1.35,
                  alinhar="esquerda", tracking=0.0, nome=None, papel="texto", sobre=()):
        """Texto em várias linhas com quebra automática. Retorna a caixa ocupada."""
        size = self.tamanho(fonte, cap, pt)
        caph = cap_ratio(fonte) * size
        lead = size * entrelinha
        linhas = []
        for bloco in texto.split("\n"):
            palavras = bloco.split(" ")
            atual = ""
            for w in palavras:
                teste = (atual + " " + w).strip()
                b, _ = medir(teste, fonte, size, tracking)
                if b.w <= largura or not atual:
                    atual = teste
                else:
                    linhas.append(atual)
                    atual = w
            linhas.append(atual)
        y = y_topo - caph
        caixas = []
        for ln in linhas:
            if ln:
                ax = {"esquerda": x, "centro": x + largura / 2, "direita": x + largura}[alinhar]
                caixas.append(self.texto(ln, fonte, ax, y, pt=size * CM, cor_texto=cor_texto, tracking=tracking,
                                         alinhar=alinhar, papel=papel, registrar=False))
            y -= lead
        if not caixas:
            return Caixa(x, y_topo, x, y_topo)
        box = Caixa(min(b.x0 for b in caixas), min(b.y0 for b in caixas), max(b.x1 for b in caixas), max(b.y1 for b in caixas))
        self._reg(nome or texto[:24], papel, box, sobre, cap=caph, texto=texto, fonte=fonte, linhas=len(linhas))
        return box

    def preco(self, valor, fonte, x, y_base, cap=None, largura_max=None, altura_max=None, cor_texto="#000000",
              moeda="R$", alinhar="esquerda", tracking=None, prop_moeda=0.27, prop_centavos=0.45, respiro=0.05,
              nome="preco", papel="texto", desenhar=True, de=None, cor_de=None):
        """Preço de varejo: 'R$' pequeno no alto, inteiro gigante, ',99' sobrescrito.

        valor: "99,99" (ou "99" sem centavos). Informe cap (altura do inteiro) e/ou limites
        largura_max / altura_max (cm) — usa o maior tamanho que cabe nos dois.
        respiro: espaço entre partes, como fração do cap. Retorna dict com caixas e 'tudo'.
        desenhar=False só calcula: retorna {"cap", "largura"} para você posicionar antes de desenhar.
        de: preço anterior ("59,90") — desenha "de R$ 59,90 por" riscado acima do preço (só se for o
            preço praticado de verdade; ver references/obrigatorios.md). Ocupa ~25 % do cap acima do topo.
        """
        inteiro, _, cent = valor.partition(",")
        cent = "," + cent if cent else ""
        if tracking is None:  # proporcional ao tamanho: ~1 % do cap do inteiro
            tracking = 0.01 * (cap or altura_max or 10)

        def largura(c):
            w = 0.0
            if moeda:
                w += self.medir(moeda, fonte, cap=c * prop_moeda, tracking=tracking * prop_moeda).w + respiro * c
            w += self.medir(inteiro, fonte, cap=c, tracking=tracking).w
            if cent:
                w += respiro * c * 0.8 + self.medir(cent, fonte, cap=c * prop_centavos, tracking=tracking * prop_centavos).w
            return w

        fator_h = 1.25 if de else 1.0
        caps = [v for v in (cap, (altura_max / fator_h) if altura_max else None) if v]
        if largura_max:
            caps.append(largura_max / (largura(10.0) / 10.0))
        if not caps:
            raise ValueError("informe cap, largura_max ou altura_max")
        c_ = min(caps)
        total = largura(c_)
        if not desenhar:
            return {"cap": c_, "largura": total}
        x0 = {"esquerda": x, "direita": x - total, "centro": x - total / 2}[alinhar]
        topo = y_base + c_
        out = {}
        cx = x0
        if moeda:
            out["moeda"] = self.texto(moeda, fonte, cx, topo, cap=c_ * prop_moeda, cor_texto=cor_texto, tracking=tracking * prop_moeda,
                                      ancora="topo", nome=f"{nome}-moeda", papel=papel)
            cx = out["moeda"].x1 + respiro * c_
        out["inteiro"] = self.texto(inteiro, fonte, cx, y_base, cap=c_, cor_texto=cor_texto, tracking=tracking,
                                    nome=f"{nome}-inteiro", papel=papel)
        if cent:
            out["centavos"] = self.texto(cent, fonte, out["inteiro"].x1 + respiro * c_ * 0.8, topo, cap=c_ * prop_centavos,
                                         cor_texto=cor_texto, tracking=tracking * prop_centavos, ancora="topo",
                                         nome=f"{nome}-centavos", papel=papel)
        if de:
            cde = c_ * 0.16
            yb = topo + c_ * 0.09
            corx = cor_de or cor_texto
            t1 = self.texto("de", fonte, x0, yb, cap=cde, cor_texto=corx, tracking=tracking * 0.16, nome=f"{nome}-de", papel=papel)
            val = f"{moeda} {de}" if moeda else de
            t2 = self.texto(val, fonte, t1.x1 + cde * 0.5, yb, cap=cde, cor_texto=corx, tracking=tracking * 0.16,
                            nome=f"{nome}-de-valor", papel=papel)
            self.linha(t2.x0 - cde * 0.1, yb + cde * 0.45, t2.x1 + cde * 0.1, yb + cde * 0.45, corx, espessura=cde * 0.13)
            t3 = self.texto("por", fonte, t2.x1 + cde * 0.5, yb, cap=cde, cor_texto=corx, tracking=tracking * 0.16,
                            nome=f"{nome}-por", papel=papel)
            out["de"] = Caixa(t1.x0, t1.y0, t3.x1, t3.y1)
        bs = [v for v in out.values() if isinstance(v, Caixa)]
        out["tudo"] = Caixa(min(b.x0 for b in bs), min(b.y0 for b in bs), max(b.x1 for b in bs), max(b.y1 for b in bs))
        out["cap"] = c_
        return out

    # ---- imagens ----
    def imagem(self, caminho, x, y, w=None, h=None, opacidade=1.0, nome=None, papel="conteudo", sobre=()):
        """Logo/ilustração PNG/JPG mantendo proporção. Informe w ou h (cm)."""
        img = Image.open(caminho)
        iw, ih = img.size
        if w is None and h is None:
            raise ValueError("informe w ou h")
        if w is None:
            w = h * iw / ih
        if h is None:
            h = w * ih / iw
        self.c.saveState()
        if opacidade < 1:
            self.c.setFillAlpha(opacidade)
        self.c.drawImage(ImageReader(img), x * CM, y * CM, w * CM, h * CM, mask="auto")
        self.c.restoreState()
        if self.modo_cor == "cmyk":
            self.avisos.append(f"CMYK: '{os.path.basename(caminho)}' ficou em RGB (imagem com transparência); "
                               "para CMYK puro, peça o logo vetorial ou desenhe-o com formas do kit")
        dpi = iw / (w / 2.54)
        if dpi < self.faixa["dpi_min"]:
            self.avisos.append(f"imagem '{os.path.basename(caminho)}' com {dpi:.0f} dpi efetivos (mínimo {self.faixa['dpi_min']} para {self.faixa['nome']})")
        b = Caixa(x, y, x + w, y + h)
        self._reg(nome or os.path.basename(caminho), papel, b, sobre, dpi=round(dpi))
        return b

    def foto(self, caminho, x, y, w, h, foco=(0.5, 0.5), zoom=1.0, opacidade=1.0, fades=(), escurecer=(),
             contraste_foto=1.0, saturacao=1.0, brilho=1.0, compor_sobre=None, dpi_max=None, nome=None,
             papel="decorativo", sobre=()):
        """Foto preenchendo a área (x, y, w, h) como 'cover', com opacidade e fades.

        foco: ponto da foto (0-1, 0-1; origem no canto superior esquerdo da foto) que fica no centro da área.
        zoom: >1 aproxima.
        fades: lista de (lado, inicio, fim) em cm do banner. lado ∈ direita|esquerda|topo|base.
               ("direita", 60, 110) = foto plena até x=60 e some em x=110 (fade-x).
               ("base", 30, 12)    = plena acima de y=30 e some em y=12.
        escurecer: lista de (Caixa, força 0-1, raio cm) — reduz a foto ao redor de textos
                   (sombra suave que garante leitura sobre a foto).
        compor_sobre: cor de fundo para achatar a transparência (PDF bem menor, embute JPEG).
                      Use quando o que está atrás da foto é cor lisa.
        Retorna a caixa. Avisa se a resolução efetiva ficar abaixo do mínimo para a distância.
        """
        src = ImageOps.exif_transpose(Image.open(caminho)).convert("RGB")
        sw, sh = src.size
        A = w / h
        if sw / sh > A:
            cw, ch = sh * A, sh
        else:
            cw, ch = sw, sw / A
        cw, ch = cw / zoom, ch / zoom
        fx, fy = foco
        cx0 = min(max(fx * sw - cw / 2, 0), sw - cw)
        cy0 = min(max(fy * sh - ch / 2, 0), sh - ch)
        crop = src.crop((int(round(cx0)), int(round(cy0)), int(round(cx0 + cw)), int(round(cy0 + ch))))
        dpi_nat = crop.width / (w / 2.54)
        alvo = dpi_max or max(self.faixa["dpi"], 150)
        if dpi_nat > alvo:
            nw = int(round(w / 2.54 * alvo))
            crop = crop.resize((nw, int(round(nw * crop.height / crop.width))), Image.LANCZOS)
        dpi_ef = crop.width / (w / 2.54)
        if contraste_foto != 1:
            crop = ImageEnhance.Contrast(crop).enhance(contraste_foto)
        if saturacao != 1:
            crop = ImageEnhance.Color(crop).enhance(saturacao)
        if brilho != 1:
            crop = ImageEnhance.Brightness(crop).enhance(brilho)

        pw, ph = crop.size
        X = x + (np.arange(pw) + 0.5) / pw * w
        Y = y + h - (np.arange(ph) + 0.5) / ph * h
        X, Y = np.meshgrid(X, Y)
        a = np.full(X.shape, float(opacidade), dtype=np.float32)

        def smooth(e0, e1, v):
            t = np.clip((v - e0) / (e1 - e0), 0, 1)
            return t * t * (3 - 2 * t)

        for lado, ini, fim in fades:
            if lado == "direita":
                a *= 1 - smooth(ini, fim, X)
            elif lado == "esquerda":
                a *= smooth(fim, ini, X)
            elif lado == "topo":
                a *= 1 - smooth(ini, fim, Y)
            elif lado == "base":
                a *= smooth(fim, ini, Y)
            else:
                raise ValueError("lado do fade: direita|esquerda|topo|base")
        for caixa, forca, raio in escurecer:
            cb = caixa if isinstance(caixa, Caixa) else Caixa(*caixa)
            dx = np.maximum(np.maximum(cb.x0 - X, X - cb.x1), 0)
            dy = np.maximum(np.maximum(cb.y0 - Y, Y - cb.y1), 0)
            d = np.sqrt(dx * dx + dy * dy)
            a *= 1 - forca * (1 - smooth(0.0, raio, d))
        alpha = np.clip(a, 0, 1)

        tmp = os.path.join(self._tmp, f"foto_{len(self.fotos)}")
        if self.modo_cor == "cmyk" and compor_sobre is None and alpha.min() < 0.999:
            compor_sobre = self._ultimo_fundo
            self.avisos.append(f"CMYK: a transparência da foto foi achatada sobre {compor_sobre} (gradientes atrás dela não aparecem); "
                               "passe compor_sobre= para escolher a cor")
        if compor_sobre is not None or alpha.min() >= 0.999:
            rgb = np.asarray(crop, dtype=np.float32)
            if compor_sobre is not None:
                bg = np.array([v * 255 for v in _rgb01(compor_sobre)], dtype=np.float32)
                rgb = rgb * alpha[..., None] + bg * (1 - alpha[..., None])
            im_out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
            if self.modo_cor == "cmyk":
                from PIL import ImageCms

                im_out = ImageCms.applyTransform(im_out, self._xf_foto)
            im_out.save(tmp + ".jpg", quality=92, subsampling=0)
            self.c.drawImage(tmp + ".jpg", x * CM, y * CM, w * CM, h * CM)
        else:
            rgba = np.dstack([np.asarray(crop, dtype=np.uint8), (alpha * 255).astype(np.uint8)])
            self.c.drawImage(ImageReader(Image.fromarray(rgba, "RGBA")), x * CM, y * CM, w * CM, h * CM, mask="auto")

        info = {"arquivo": os.path.basename(caminho), "dpi_efetivo": round(dpi_ef), "dpi_nativo": round(dpi_nat)}
        self.fotos.append(info)
        if dpi_ef < self.faixa["dpi_min"]:
            self.avisos.append(f"foto '{info['arquivo']}' com {dpi_ef:.0f} dpi efetivos — abaixo do mínimo {self.faixa['dpi_min']} para {self.faixa['nome']}")
        b = Caixa(x, y, x + w, y + h)
        self._reg(nome or info["arquivo"], papel, b, sobre, **info)
        return b

    def qrcode(self, dados, x, y, lado, cor_qr="#000000", cor_fundo="#FFFFFF", distancia_scan_m=None, nome="qrcode", sobre=()):
        """QR code vetorial com zona de silêncio. Regra: lado ≥ distância de escaneamento ÷ 10 (e ≥ 1,5 cm).

        distancia_scan_m: de onde a pessoa aponta o celular (padrão: a distância da peça, limitada a 2 m —
        ninguém escaneia uma faixa a 15 m; a pessoa se aproxima).
        """
        from reportlab.graphics.shapes import STATE_DEFAULTS
        STATE_DEFAULTS["fontName"] = FONTE_PADRAO  # senão o desenho referencia Times-Roman (não incorporada)
        w = rl_qr.QrCodeWidget(dados, barFillColor=self._cor(cor_qr), barStrokeColor=self._cor(cor_qr))
        b = w.getBounds()
        bw, bh = b[2] - b[0], b[3] - b[1]
        d = Drawing(lado * CM, lado * CM, transform=[lado * CM / bw, 0, 0, lado * CM / bh, 0, 0])
        d.add(w)
        self.retangulo(x, y, lado, lado, preenchimento=cor_fundo)
        renderPDF.draw(d, self.c, x * CM, y * CM)
        if distancia_scan_m is not None:
            dscan = distancia_scan_m
        else:  # peça de mão: o celular chega a ~20 cm; peça de parede: a pessoa para a até 2 m
            dscan = 0.2 if self.distancia_m <= 1.0 else min(self.distancia_m, 2.0)
        minimo = max(1.5, dscan * 10.0)
        if lado < minimo - 1e-6:
            self.avisos.append(f"QR code com {lado:.1f} cm — para escanear a {dscan:g} m use ≥ {minimo:.1f} cm")
        box = Caixa(x, y, x + lado, y + lado)
        self._reg(nome, "conteudo", box, sobre)
        return box

    def relatorio_cores(self, cores: dict):
        """Atalho para relatorio_cores() — contraste entre as cores da paleta, com daltonismo."""
        return relatorio_cores(cores)

    # ---- checagens ----
    def checar(self) -> list[str]:
        prob = []
        textos = [e for e in self.elementos if e.papel in ("texto", "detalhe", "conteudo")]
        for i in range(len(textos)):
            for j in range(i + 1, len(textos)):
                a, b = textos[i], textos[j]
                if a.nome.split(":")[0] != b.nome.split(":")[0]:
                    continue  # páginas diferentes
                if b.nome in a.sobre or a.nome in b.sobre:
                    continue
                if a.caixa.cruza(b.caixa):
                    prob.append(f"sobreposição: {a.nome} × {b.nome}")
        util = self.area_util
        for e in textos:
            cb = e.caixa
            tol = max(0.1 * e.cap_cm, 0.02) if e.cap_cm else 0.0  # overshoot de O/C/S e ascendentes (d, l, t)
            if cb.x0 < util.x0 - tol or cb.y0 < util.y0 - tol or cb.x1 > util.x1 + tol or cb.y1 > util.y1 + tol:
                prob.append(f"fora da margem de segurança ({self.seguranca} cm): {e.nome} {tuple(round(v, 2) for v in cb.tupla())}")
        lmin = letra_minima_cm(self.distancia_m)
        for e in self.elementos:
            if e.papel == "texto" and e.cap_cm is not None and e.cap_cm < lmin - 1e-6:
                prob.append(f"letra pequena para {self.distancia_m:g} m: {e.nome} (maiúscula {e.cap_cm:.2f} cm; mínimo {lmin:.2f} cm) — aumente ou marque papel='detalhe'")
        caps = [e.cap_cm for e in self.elementos if e.cap_cm and e.papel == "texto"]
        if caps and max(caps) < letra_impacto_cm(self.distancia_m) and self.distancia_m > 1.5:
            prob.append(f"mensagem principal pequena: maior maiúscula {max(caps):.1f} cm; para impacto a {self.distancia_m:g} m use ≥ {letra_impacto_cm(self.distancia_m):.1f} cm")
        return prob + self.avisos

    def relatorio(self) -> str:
        lin = [
            f"Peça {self.W:g} × {self.H:g} cm · {self.material} · sangria {self.sangria:g} cm · segurança {self.seguranca:g} cm · "
            f"{self.modo_cor.upper()}" + (f" ({os.path.basename(self.icc)})" if self.icc else ""),
            f"Distância de leitura {self.distancia_m:g} m ({self.faixa['nome']}) → {self.faixa['dpi']} dpi recomendados; "
            f"letra mínima {letra_minima_cm(self.distancia_m):.2f} cm, impacto {letra_impacto_cm(self.distancia_m):.1f} cm",
            "Textos (maior → menor): maiúscula | lido com impacto até | legível até",
        ]
        for e in sorted([e for e in self.elementos if e.cap_cm], key=lambda e: -e.cap_cm):
            imp, lim = distancia_legivel_m(e.cap_cm)
            lin.append(f"  {e.nome[:34]:34s} {e.cap_cm:6.2f} cm | {imp:6.1f} m | {lim:6.1f} m  [{e.papel}]")
        for f in self.fotos:
            lin.append(f"  foto {f['arquivo']}: {f['dpi_efetivo']} dpi efetivos")
        return "\n".join(lin)

    def salvar(self, checar=True) -> list[str]:
        self._finalizar_pagina()
        self.c.showPage()
        self.c.save()
        prob = self.checar() if checar else []
        spec = {
            "arquivo": os.path.basename(self.arquivo),
            "largura_cm": self.W,
            "altura_cm": self.H,
            "material": self.material,
            "sangria_cm": self.sangria,
            "seguranca_cm": self.seguranca,
            "distancia_m": self.distancia_m,
            "faixa": self.faixa,
            "paginas": self.pagina,
            "marcas_corte": self.marcas_corte,
            "cores": self.modo_cor,
            "perfil_icc": os.path.basename(self.icc) if self.icc else None,
            "elementos": [
                {"nome": e.nome, "papel": e.papel, "caixa": [round(v, 3) for v in e.caixa.tupla()],
                 "cap_cm": None if e.cap_cm is None else round(e.cap_cm, 3), **{k: v for k, v in e.info.items() if k != "linhas"}}
                for e in self.elementos
            ],
            "fotos": self.fotos,
            "problemas": prob,
        }
        base = os.path.splitext(self.arquivo)[0]
        with open(base + ".spec.json", "w", encoding="utf-8") as f:
            json.dump(spec, f, ensure_ascii=False, indent=2)
        print(self.relatorio())
        print("PROBLEMAS:" if prob else "PROBLEMAS: nenhum")
        for p_ in prob:
            print("  -", p_)
        return prob
