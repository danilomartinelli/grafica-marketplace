#!/usr/bin/env python3
"""Pré-impressão: confere se um arquivo está pronto para a gráfica.

  preflight.py peca.pdf                         # usa o .spec.json ao lado, se existir
  preflight.py arte.pdf --largura 200 --altura 80 --distancia 15 --material lona
  preflight.py foto-banner.jpg --largura 200 --altura 80 --distancia 15

PDF: tamanho final (TrimBox) e sangria, fontes incorporadas, resolução efetiva de cada
imagem, menor letra (pela altura de maiúscula) contra a distância de leitura, textos
começando dentro da margem de segurança, espaço de cor.
Imagem (JPG/PNG/TIFF): pixels, DPI no tamanho pedido, proporção.
Sai com código 1 se houver reprovação (✗); avisos (!) não reprovam.
"""
import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grafica_kit import MATERIAIS, faixa_distancia, letra_impacto_cm, letra_minima_cm  # noqa: E402
from motor_pdf import listar_fontes, listar_imagens  # noqa: E402

PT_CM = 2.54 / 72
OK, AV, ER = "✓", "!", "✗"


def linha(status, msg, out):
    out.append((status, msg))


def checar_pdf(path, esp, out):
    from pypdf import PdfReader

    r = PdfReader(path)
    n = len(r.pages)
    pg = r.pages[0]
    media = [float(v) for v in pg.mediabox]
    trim = [float(v) for v in pg.trimbox] if "/TrimBox" in pg else None
    bleed = [float(v) for v in pg.bleedbox] if "/BleedBox" in pg else None
    ref = trim or media
    W = (ref[2] - ref[0]) * PT_CM
    H = (ref[3] - ref[1]) * PT_CM
    linha(OK if trim else AV, f"{n} página(s); tamanho final {W:.1f} × {H:.1f} cm" + ("" if trim else " (sem TrimBox: usando a página inteira)"), out)

    if esp.get("largura") and esp.get("altura"):
        ok = abs(W - esp["largura"]) < 0.15 and abs(H - esp["altura"]) < 0.15
        girado = abs(W - esp["altura"]) < 0.15 and abs(H - esp["largura"]) < 0.15
        linha(OK if ok else ER, f"tamanho pedido {esp['largura']:g} × {esp['altura']:g} cm" + ("" if ok else (" — está girado" if girado else f" — arquivo tem {W:.1f} × {H:.1f}")), out)

    sang = 0.0
    if trim and bleed:
        sang = min(trim[0] - bleed[0], trim[1] - bleed[1], bleed[2] - trim[2], bleed[3] - trim[3]) * PT_CM
    elif trim:
        sang = min(trim[0] - media[0], trim[1] - media[1], media[2] - trim[2], media[3] - trim[3]) * PT_CM
    if esp.get("sangria") is not None:
        st = OK if sang + 1e-3 >= esp["sangria"] else ER
        linha(st, f"sangria {sang*10:.1f} mm (esperado ≥ {esp['sangria']*10:.0f} mm)", out)
    else:
        linha(OK if sang > 0 else AV, f"sangria {sang*10:.1f} mm", out)

    # fontes
    try:
        emb = listar_fontes(path)
        nao = [nm for nm, e in emb if not e]
        linha(OK if not nao else ER, f"{len(emb)} fonte(s), " + ("todas incorporadas" if not nao else f"NÃO incorporadas: {', '.join(nao)}"), out)
    except Exception as e:  # noqa: BLE001
        linha(AV, f"não consegui listar fontes ({e})", out)

    # imagens
    dist = esp.get("distancia")
    fx = faixa_distancia(dist) if dist else None
    try:
        imgs = listar_imagens(path)
        if not imgs:
            linha(OK, "sem imagens (100% vetorial)", out)
        for im in imgs:
            if fx:
                st = OK if im["ppi"] >= fx["dpi_min"] else ER
                extra = f" (mínimo {fx['dpi_min']} para {fx['nome']}; ideal {fx['dpi']})"
            else:
                st = OK if im["ppi"] >= 150 else AV
                extra = ""
            linha(st, f"imagem p{im['pag']} {im['w']}×{im['h']} px, {im['cor']}, {im['ppi']} dpi efetivos{extra}", out)
        cores = sorted({i["cor"] for i in imgs})
        if "rgb" in cores:
            linha(AV, "imagens em RGB — gráfica rápida/digital aceita; para offset, peça à gráfica a conversão CMYK com o perfil dela", out)
    except Exception as e:  # noqa: BLE001
        linha(AV, f"não consegui listar imagens ({e})", out)

    # textos: menor maiúscula e posição de início
    runs = []

    def visitor(text, cm, tm, font_dict, font_size):
        if not text or not text.strip() or not font_size:
            return
        sx = math.hypot(tm[0], tm[1]) * math.hypot(cm[0], cm[1])
        size_pt = font_size * sx
        cap = 0.7
        try:
            fd = font_dict.get("/FontDescriptor") if font_dict else None
            if fd is None and font_dict and "/DescendantFonts" in font_dict:
                fd = font_dict["/DescendantFonts"][0].get_object().get("/FontDescriptor")
            if fd is not None:
                fd = fd.get_object()
                if "/CapHeight" in fd and float(fd["/CapHeight"]) > 0:
                    cap = float(fd["/CapHeight"]) / 1000
        except Exception:  # noqa: BLE001
            pass
        x = cm[0] * tm[4] + cm[2] * tm[5] + cm[4]
        y = cm[1] * tm[4] + cm[3] * tm[5] + cm[5]
        runs.append({"txt": text.strip()[:30], "cap_cm": size_pt * cap * PT_CM, "x": x, "y": y, "size_cm": size_pt * PT_CM})

    for i, page in enumerate(r.pages):
        try:
            page.extract_text(visitor_text=visitor)
        except Exception:  # noqa: BLE001
            pass
    if runs:
        menor = min(runs, key=lambda q: q["cap_cm"])
        maior = max(runs, key=lambda q: q["cap_cm"])
        if dist:
            lmin = letra_minima_cm(dist)
            peq = [q for q in runs if q["cap_cm"] < lmin]
            linha(OK if not peq else AV,
                  f"menor letra: '{menor['txt']}' maiúscula {menor['cap_cm']:.2f} cm (mínimo {lmin:.2f} cm a {dist:g} m)"
                  + (f" — {len(peq)} trecho(s) abaixo; ok só se forem detalhes para quem chega perto" if peq else ""), out)
            limp = letra_impacto_cm(dist)
            linha(OK if maior["cap_cm"] >= limp or dist <= 1.5 else AV,
                  f"maior letra: '{maior['txt']}' maiúscula {maior['cap_cm']:.1f} cm (impacto a {dist:g} m pede ≥ {limp:.1f} cm)", out)
        else:
            linha(OK, f"menor letra '{menor['txt']}' {menor['cap_cm']:.2f} cm; maior '{maior['txt']}' {maior['cap_cm']:.1f} cm", out)
        seg = esp.get("seguranca")
        if seg is not None and trim:
            fora = []
            for q in runs:
                xc = (q["x"] - trim[0]) * PT_CM
                yc = (q["y"] - trim[1]) * PT_CM
                tol = 0.12 * q["size_cm"] + 0.05  # a origem do texto fica antes da tinta (bearing lateral)
                if xc < seg - tol or yc < seg - tol or xc > W - seg or yc > H - seg:
                    fora.append(q["txt"])
            linha(OK if not fora else ER, f"textos começam dentro da margem de segurança ({seg:g} cm)" if not fora
                  else f"texto começando fora da margem de segurança ({seg:g} cm): {', '.join(fora[:6])}", out)
    else:
        linha(AV, "nenhum texto vivo encontrado (texto em curvas ou só imagem) — confira a letra mínima visualmente", out)


def checar_imagem(path, esp, out):
    from PIL import Image

    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(path)
    w, h = im.size
    dpi_meta = im.info.get("dpi", (None, None))[0]
    linha(OK, f"{w}×{h} px ({w*h/1e6:.1f} MP), modo {im.mode}, DPI nos metadados: {dpi_meta and round(dpi_meta)}", out)
    if esp.get("largura") and esp.get("altura"):
        dpi_ef = min(w / (esp["largura"] / 2.54), h / (esp["altura"] / 2.54))
        prop_arq, prop_ped = w / h, esp["largura"] / esp["altura"]
        linha(OK if abs(prop_arq / prop_ped - 1) < 0.01 else ER,
              f"proporção {prop_arq:.3f} (pedido {prop_ped:.3f})", out)
        if esp.get("distancia"):
            fx = faixa_distancia(esp["distancia"])
            st = OK if dpi_ef >= fx["dpi_min"] else ER
            linha(st, f"{dpi_ef:.0f} dpi no tamanho {esp['largura']:g}×{esp['altura']:g} cm (mínimo {fx['dpi_min']}, ideal {fx['dpi']} para {fx['nome']})", out)
        else:
            linha(OK, f"{dpi_ef:.0f} dpi no tamanho {esp['largura']:g}×{esp['altura']:g} cm", out)
        if im.mode == "CMYK":
            linha(OK, "CMYK", out)
    else:
        if dpi_meta:
            linha(OK, f"no DPI dos metadados imprime {w/dpi_meta*2.54:.1f} × {h/dpi_meta*2.54:.1f} cm", out)
        linha(AV, "informe --largura/--altura para checar resolução no tamanho final", out)
    linha(AV, "imagem não tem sangria/segurança declaradas — confira se textos estão longe das bordas", out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("arquivo")
    ap.add_argument("--largura", type=float)
    ap.add_argument("--altura", type=float)
    ap.add_argument("--distancia", type=float)
    ap.add_argument("--material", choices=list(MATERIAIS))
    ap.add_argument("--sangria", type=float)
    ap.add_argument("--seguranca", type=float)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    esp = {}
    spec_path = os.path.splitext(a.arquivo)[0] + ".spec.json"
    if os.path.exists(spec_path):
        s = json.load(open(spec_path, encoding="utf-8"))
        esp = {"largura": s["largura_cm"], "altura": s["altura_cm"], "distancia": s["distancia_m"],
               "sangria": s["sangria_cm"], "seguranca": s["seguranca_cm"]}
    if a.material:
        esp.setdefault("sangria", MATERIAIS[a.material][0])
        esp.setdefault("seguranca", MATERIAIS[a.material][1])
    for k in ("largura", "altura", "distancia", "sangria", "seguranca"):
        v = getattr(a, k)
        if v is not None:
            esp[k] = v

    out = []
    if a.arquivo.lower().endswith(".pdf"):
        checar_pdf(a.arquivo, esp, out)
    else:
        checar_imagem(a.arquivo, esp, out)

    reprovado = any(s == ER for s, _ in out)
    if a.json:
        print(json.dumps({"arquivo": a.arquivo, "esperado": esp, "itens": [{"status": s, "msg": m} for s, m in out],
                          "aprovado": not reprovado}, ensure_ascii=False, indent=2))
    else:
        print(f"Pré-impressão: {a.arquivo}")
        for s, m in out:
            print(f"  {s} {m}")
        print("RESULTADO:", "REPROVADO — corrigir os itens ✗" if reprovado else "APROVADO (veja os avisos !)")
    sys.exit(1 if reprovado else 0)


if __name__ == "__main__":
    main()
