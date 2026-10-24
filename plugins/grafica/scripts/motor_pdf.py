#!/usr/bin/env python3
"""Leitura e renderização de PDF para os scripts do kit, com ou sem o poppler instalado.

- Renderizar uma região da página no DPI exato: usa o `pdftoppm` (poppler) se existir;
  senão o pypdfium2 (pacote pip, sem programa extra para instalar).
- Listar imagens com o DPI efetivo: `pdfimages -list` se existir; senão o pypdfium2.
- Listar fontes e se estão incorporadas: sempre pelo pypdf (não depende do poppler).

GRAFICA_MOTOR=pdfium força o caminho sem poppler (útil para testar).
"""
import os
import shutil
import struct
import subprocess
import sys

# Windows: saída para o terminal/pipe em UTF-8 (✓ ✗ × ã) sem quebrar no cp1252
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass


def usa_poppler(ferramenta="pdftoppm"):
    if os.environ.get("GRAFICA_MOTOR", "").lower() == "pdfium":
        return False
    return shutil.which(ferramenta) is not None


def motor_atual():
    return "poppler" if usa_poppler() else "pdfium"


def ajustar_dpi_jpeg(caminho, dpi):
    b = bytearray(open(caminho, "rb").read())
    if b[0:4] == b"\xff\xd8\xff\xe0" and b[6:11] == b"JFIF\x00":
        b[13] = 1
        b[14:16] = struct.pack(">H", int(round(dpi)))
        b[16:18] = struct.pack(">H", int(round(dpi)))
        open(caminho, "wb").write(b)


def renderizar(pdf, pagina, regiao, media, dpi, formato, saida_base, qualidade):
    """Renderiza `regiao` (x0, y0, x1, y1 em pt, coordenadas do PDF) da página `pagina` (1 = primeira).

    Devolve (caminho, largura_px, altura_px). O tamanho em pixels é exato:
    round(largura_pt / 72 × dpi) × round(altura_pt / 72 × dpi).
    """
    x0, y0, x1, y1 = regiao
    W = round((x1 - x0) / 72 * dpi)
    H = round((y1 - y0) / 72 * dpi)
    caminho = saida_base + (".jpg" if formato == "jpg" else ".png")
    if usa_poppler("pdftoppm"):
        X = round((x0 - media[0]) / 72 * dpi)
        Y = round((media[3] - y1) / 72 * dpi)
        cmd = ["pdftoppm", "-r", f"{dpi}", "-f", str(pagina), "-l", str(pagina), "-x", str(X), "-y", str(Y),
               "-W", str(W), "-H", str(H), "-singlefile", "-aa", "yes", "-aaVector", "yes"]
        cmd += ["-jpeg", "-jpegopt", f"quality={qualidade},optimize=y"] if formato == "jpg" else ["-png"]
        subprocess.run(cmd + [pdf, saida_base], check=True)
        if formato == "jpg":
            ajustar_dpi_jpeg(caminho, dpi)
        return caminho, W, H

    import pypdfium2 as pdfium
    from PIL import Image

    Image.MAX_IMAGE_PIXELS = None
    doc = pdfium.PdfDocument(pdf)
    try:
        pg = doc[pagina - 1]
        # o pdfium desenha a CropBox (que, sem CropBox, é a MediaBox); o recorte é medido a partir dela
        l, b, r, t = pg.get_cropbox()
        corte = (max(0.0, x0 - l), max(0.0, y0 - b), max(0.0, r - x1), max(0.0, t - y1))
        im = pg.render(scale=dpi / 72, crop=corte, may_draw_forms=False).to_pil().convert("RGB")
    finally:
        doc.close()
    if im.size != (W, H):  # diferença de arredondamento de no máximo 1–2 px
        im = im.resize((W, H), Image.LANCZOS)
    if formato == "jpg":
        im.save(caminho, "JPEG", quality=int(qualidade), optimize=True, dpi=(dpi, dpi))
    else:
        im.save(caminho, "PNG", dpi=(dpi, dpi))
    return caminho, W, H


_CORES_PDFIUM = {1: "gray", 2: "rgb", 3: "cmyk", 4: "gray", 5: "rgb", 6: "lab", 8: "sep", 9: "devn", 10: "index"}


def listar_imagens(pdf):
    """Lista as imagens desenhadas: [{"pag", "w", "h", "cor", "ppi"}], com o DPI efetivo no tamanho impresso."""
    if usa_poppler("pdfimages"):
        out = subprocess.run(["pdfimages", "-list", pdf], capture_output=True, text=True, check=True).stdout
        imgs = []
        for l in out.splitlines()[2:]:
            p = l.split()
            if len(p) >= 14 and p[2] == "image":
                imgs.append({"pag": int(p[0]), "w": int(p[3]), "h": int(p[4]), "cor": p[5],
                             "ppi": min(int(p[12]), int(p[13]))})
        return imgs

    import pypdfium2 as pdfium
    import pypdfium2.raw as pdfium_c

    imgs = []
    doc = pdfium.PdfDocument(pdf)
    try:
        for i in range(len(doc)):
            pg = doc[i]
            for obj in pg.get_objects(filter=(pdfium_c.FPDF_PAGEOBJ_IMAGE,), max_depth=15):
                md = obj.get_metadata()
                cor = _CORES_PDFIUM.get(md.colorspace)
                if cor is None:  # ICCBased e afins: deduz pelos bits por pixel
                    cor = {8: "gray", 24: "rgb", 32: "cmyk"}.get(md.bits_per_pixel, "icc")
                ppi = int(round(min(md.horizontal_dpi, md.vertical_dpi)))
                imgs.append({"pag": i + 1, "w": int(md.width), "h": int(md.height), "cor": cor, "ppi": ppi})
    finally:
        doc.close()
    return imgs


def tem_imagens(pdf):
    try:
        return bool(listar_imagens(pdf))
    except Exception:  # noqa: BLE001
        return True


def listar_fontes(pdf):
    """[(nome, incorporada: bool)] de todas as fontes usadas, inclusive dentro de Form XObjects."""
    from pypdf import PdfReader

    r = PdfReader(pdf)
    vistas, res = set(), []

    def descritor(f):
        if f.get("/Subtype") == "/Type0" and "/DescendantFonts" in f:
            f = f["/DescendantFonts"][0].get_object()
        fd = f.get("/FontDescriptor")
        return fd.get_object() if fd is not None else None

    def visitar(recursos, profundidade=0):
        if recursos is None or profundidade > 10:
            return
        recursos = recursos.get_object()
        fontes = recursos.get("/Font")
        if fontes is not None:
            for _, ref in fontes.get_object().items():
                chave = getattr(ref, "idnum", id(ref))
                if chave in vistas:
                    continue
                vistas.add(chave)
                f = ref.get_object()
                nome = str(f.get("/BaseFont", "(sem nome)")).lstrip("/")
                if f.get("/Subtype") == "/Type3":
                    res.append((nome, True))
                    continue
                fd = descritor(f)
                emb = fd is not None and any(k in fd for k in ("/FontFile", "/FontFile2", "/FontFile3"))
                res.append((nome, emb))
        xobjs = recursos.get("/XObject")
        if xobjs is not None:
            for _, ref in xobjs.get_object().items():
                x = ref.get_object()
                if x.get("/Subtype") == "/Form":
                    visitar(x.get("/Resources"), profundidade + 1)

    for pg in r.pages:
        visitar(pg.get("/Resources"))
    return res
