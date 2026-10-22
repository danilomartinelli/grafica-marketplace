#!/usr/bin/env python3
"""Gera imagens de uma peça em PDF no DPI certo, com o tamanho exato em pixels.

Exemplos
  rasterizar.py banner.pdf                      # DPI da distância (lido do .spec.json), formato automático
  rasterizar.py banner.pdf --dpi 300            # força 300 dpi
  rasterizar.py banner.pdf --canva              # versão para subir no Canva (≤ 100 MP, ≤ 25 MB, JPEG)
  rasterizar.py banner.pdf --previa             # prévia leve (~1800 px) para conferir na conversa
  rasterizar.py banner.pdf --previa --guias     # prévia com linhas de corte, sangria e segurança
  rasterizar.py cartao.pdf --pagina 2           # verso
  rasterizar.py banner.pdf --simular 15         # como um olho 20/20 vê a peça a 15 m (teste dos 3 segundos)
  rasterizar.py banner.pdf --daltonismo         # folha com a peça vista com deuteranopia, protanopia, tritanopia e em cinza

Por padrão recorta na linha de corte (TrimBox). --com-sangria inclui a sangria.
Formato automático: JPEG se o PDF tiver fotos (PNG com foto fica enorme), PNG se for só vetor.
"""
import argparse
import json
import math
import os
import struct
import subprocess
import sys

from pypdf import PdfReader

CANVA_MAX_PX = 100_000_000
CANVA_MAX_BYTES = 25 * 1024 * 1024



def _fonte_rotulo(tamanho):
    """Fonte dos rótulos da folha de daltonismo: a mesma busca de fontes do kit (sem caminho fixo)."""
    from PIL import ImageFont
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from grafica_kit import fontes_disponiveis, _index_fonts
        for nome in ("WorkSans-Bold", "InstrumentSans-Bold"):
            if nome in fontes_disponiveis():
                return ImageFont.truetype(_index_fonts()[nome], tamanho)
    except Exception:
        pass
    return ImageFont.load_default()

def caixas(pdf, pagina):
    pg = PdfReader(pdf).pages[pagina - 1]
    media = [float(v) for v in pg.mediabox]
    trim = [float(v) for v in (pg.trimbox if "/TrimBox" in pg else pg.mediabox)]
    bleed = [float(v) for v in (pg.bleedbox if "/BleedBox" in pg else pg.mediabox)]
    return media, trim, bleed


def tem_imagens(pdf):
    try:
        out = subprocess.run(["pdfimages", "-list", pdf], capture_output=True, text=True, check=True).stdout
        return any(l.split()[2:3] == ["image"] for l in out.splitlines()[2:] if l.strip())
    except Exception:
        return True


def ajustar_dpi_jpeg(caminho, dpi):
    b = bytearray(open(caminho, "rb").read())
    if b[0:4] == b"\xff\xd8\xff\xe0" and b[6:11] == b"JFIF\x00":
        b[13] = 1
        b[14:16] = struct.pack(">H", int(round(dpi)))
        b[16:18] = struct.pack(">H", int(round(dpi)))
        open(caminho, "wb").write(b)


def renderizar(pdf, pagina, regiao, media, dpi, formato, saida_base, qualidade):
    x0, y0, x1, y1 = regiao
    W = round((x1 - x0) / 72 * dpi)
    H = round((y1 - y0) / 72 * dpi)
    X = round((x0 - media[0]) / 72 * dpi)
    Y = round((media[3] - y1) / 72 * dpi)
    cmd = ["pdftoppm", "-r", f"{dpi}", "-f", str(pagina), "-l", str(pagina), "-x", str(X), "-y", str(Y),
           "-W", str(W), "-H", str(H), "-singlefile", "-aa", "yes", "-aaVector", "yes"]
    if formato == "jpg":
        cmd += ["-jpeg", "-jpegopt", f"quality={qualidade},optimize=y"]
    else:
        cmd += ["-png"]
    subprocess.run(cmd + [pdf, saida_base], check=True)
    caminho = saida_base + (".jpg" if formato == "jpg" else ".png")
    if formato == "jpg":
        ajustar_dpi_jpeg(caminho, dpi)
    return caminho, W, H


def desenhar_guias(png, regiao_px_por_cm, spec, com_sangria):
    from PIL import Image, ImageDraw

    im = Image.open(png).convert("RGB")
    d = ImageDraw.Draw(im)
    s = regiao_px_por_cm
    b = spec.get("sangria_cm", 0) if com_sangria else 0
    W, H = spec["largura_cm"], spec["altura_cm"]
    seg = spec.get("seguranca_cm", 0)

    def ret(x0, y0, x1, y1, cor, tracejado=False):
        # coordenadas em cm da área final, origem embaixo à esquerda
        px0, px1 = (x0 + b) * s, (x1 + b) * s
        py0, py1 = (H - y1 + b) * s, (H - y0 + b) * s
        if not tracejado:
            d.rectangle([px0, py0, px1, py1], outline=cor, width=2)
            return
        passo = 12
        for x in range(int(px0), int(px1), passo * 2):
            d.line([x, py0, min(x + passo, px1), py0], fill=cor, width=2)
            d.line([x, py1, min(x + passo, px1), py1], fill=cor, width=2)
        for y in range(int(py0), int(py1), passo * 2):
            d.line([px0, y, px0, min(y + passo, py1)], fill=cor, width=2)
            d.line([px1, y, px1, min(y + passo, py1)], fill=cor, width=2)

    ret(0, 0, W, H, (0, 220, 255))                       # corte
    ret(seg, seg, W - seg, H - seg, (255, 0, 200), True)  # segurança
    im.save(png)


CVD = {
    "Deuteranopia (verde)": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    "Protanopia (vermelho)": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    "Tritanopia (azul)": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}


def folha_daltonismo(a, trim, media, w_in):
    """Original + 3 tipos de daltonismo (Machado et al. 2009) + tons de cinza, numa folha só."""
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont

    base = (a.pdf[:-4] if a.pdf.lower().endswith(".pdf") else a.pdf) + "-daltonismo" + (f"-p{a.pagina}" if a.pagina > 1 else "")
    caminho, W, H = renderizar(a.pdf, a.pagina, trim, media, 900 / w_in, "png", base + "-tmp", 90)
    rgb = np.asarray(Image.open(caminho).convert("RGB"), dtype=np.float32) / 255
    os.remove(caminho)
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)

    def de_lin(x):
        x = np.clip(x, 0, 1)
        return (np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055) * 255).astype(np.uint8)

    quadros = [("Original", (rgb * 255).astype(np.uint8))]
    for nome, m in CVD.items():
        quadros.append((nome, de_lin(lin @ np.array(m, dtype=np.float32).T)))
    y = lin @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    quadros.append(("Tons de cinza (contraste de luminância)", de_lin(np.repeat(y[..., None], 3, axis=2))))

    fonte = _fonte_rotulo(22)
    cols, gap, rot = (3 if W <= H * 1.6 else 2), 16, 34
    linhas = -(-len(quadros) // cols)
    folha = Image.new("RGB", (cols * W + (cols + 1) * gap, linhas * (H + rot) + (linhas + 1) * gap), "white")
    d = ImageDraw.Draw(folha)
    for i, (nome, arr) in enumerate(quadros):
        cx, cy = gap + (i % cols) * (W + gap), gap + (i // cols) * (H + rot + gap)
        d.text((cx, cy), nome, fill=(20, 20, 20), font=fonte)
        folha.paste(Image.fromarray(arr), (cx, cy + rot))
    folha.save(base + ".png")
    print(f"{base}.png: folha de acessibilidade de cor. Se alguma informação some ou só se distingue pela cor, corrija.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--dpi", type=float)
    ap.add_argument("--formato", choices=["auto", "jpg", "png"], default="auto")
    ap.add_argument("--com-sangria", action="store_true")
    ap.add_argument("--canva", action="store_true")
    ap.add_argument("--previa", action="store_true")
    ap.add_argument("--guias", action="store_true", help="com --previa: desenha corte (ciano) e segurança (magenta)")
    ap.add_argument("--simular", type=float, metavar="METROS",
                    help="gera a peça como vista a N metros (1 px ≈ 1 minuto de arco, ampliada para conferir)")
    ap.add_argument("--daltonismo", action="store_true",
                    help="folha comparando a peça com deuteranopia, protanopia, tritanopia e em tons de cinza")
    ap.add_argument("--pagina", type=int, default=1)
    ap.add_argument("--qualidade", type=int, default=92)
    ap.add_argument("--saida")
    a = ap.parse_args()

    spec_path = os.path.splitext(a.pdf)[0] + ".spec.json"
    spec = json.load(open(spec_path, encoding="utf-8")) if os.path.exists(spec_path) else {}
    media, trim, bleed = caixas(a.pdf, a.pagina)
    com_sangria = a.com_sangria or (a.previa and a.guias)
    regiao = bleed if com_sangria else trim
    w_in, h_in = (regiao[2] - regiao[0]) / 72, (regiao[3] - regiao[1]) / 72

    if a.daltonismo:
        folha_daltonismo(a, trim, media, w_in)
        return
    if a.simular:
        from PIL import Image, ImageFilter

        px_w = (w_in * 2.54) / (a.simular * 100 * math.tan(math.radians(1 / 60)))
        dpi_sim = px_w / w_in
        base = (a.pdf[:-4] if a.pdf.lower().endswith(".pdf") else a.pdf) + f"-visto-a-{a.simular:g}m" + (f"-p{a.pagina}" if a.pagina > 1 else "")
        caminho, W, H = renderizar(a.pdf, a.pagina, trim, media, dpi_sim, "png", base, 90)
        im = Image.open(caminho).convert("RGB").filter(ImageFilter.GaussianBlur(0.6))
        fator = max(1, int(1400 / max(W, 1)))
        im = im.resize((W * fator, H * fator), Image.NEAREST)
        im.save(caminho)
        print(f"{caminho}: peça vista a {a.simular:g} m ({W}×{H} px de 'retina', ampliado ×{fator}). "
              f"O que não se lê aqui não será lido na rua.")
        return
    if a.previa:
        dpi = 1800 / w_in
        formato = "png"
        sufixo = "-previa"
    elif a.canva:
        dpi = a.dpi or spec.get("faixa", {}).get("dpi", 150)
        dpi = min(dpi, math.floor(math.sqrt(CANVA_MAX_PX / (w_in * h_in))))
        formato = "jpg"
        sufixo = f"-canva-{int(dpi)}dpi"
    else:
        dpi = a.dpi or spec.get("faixa", {}).get("dpi", 150)
        formato = a.formato if a.formato != "auto" else ("jpg" if tem_imagens(a.pdf) else "png")
        sufixo = f"-{int(dpi)}dpi"
    if spec.get("paginas", 1) > 1 or a.pagina > 1:
        sufixo += f"-p{a.pagina}"
    if a.saida:
        base = a.saida[: -len(os.path.splitext(a.saida)[1])] if a.saida.lower().endswith((".jpg", ".jpeg", ".png")) else a.saida
    else:
        base = a.pdf[:-4] + sufixo if a.pdf.lower().endswith(".pdf") else a.pdf + sufixo  # nomes com ponto (14.8x21cm) ficam intactos

    q = a.qualidade if not a.canva else 90
    caminho, W, H = renderizar(a.pdf, a.pagina, regiao, media, dpi, formato, base, q)
    while a.canva and os.path.getsize(caminho) > CANVA_MAX_BYTES and q > 60:
        q -= 8
        caminho, W, H = renderizar(a.pdf, a.pagina, regiao, media, dpi, formato, base, q)
    if a.previa and a.guias and spec:
        desenhar_guias(caminho, W / (w_in * 2.54), spec, com_sangria)

    mb = os.path.getsize(caminho) / 1e6
    print(f"{caminho}: {W}×{H} px · {dpi:.0f} dpi · {w_in*2.54:.1f}×{h_in*2.54:.1f} cm · {W*H/1e6:.1f} MP · {mb:.1f} MB"
          + (f" · JPEG q{q}" if formato == "jpg" else ""))
    if W > 8000 or H > 8000:
        print("  obs.: lado > 8000 px — o app de chat não pré-visualiza; entregue zipado ou use --previa para mostrar.")


if __name__ == "__main__":
    main()
