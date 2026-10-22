#!/usr/bin/env python3
"""Exemplo: cartão de visita 9 × 5 cm, frente e verso, com marcas de corte e QR code.

  python3 exemplo_cartao.py cartao.pdf

Peça de mão (distância ~0,4 m): o que manda é hierarquia e respiro, não tamanho de letra.
Corpo de texto ≥ 7 pt; nada a menos de 4 mm do corte; fundo de cor sangra 3 mm.
"""
import os
import sys

sys.path.insert(0, os.environ.get("GRAFICA_KIT", os.path.dirname(os.path.abspath(__file__))))  # na cópia: PYTHONPATH=RAIZ/scripts
from grafica_kit import Peca  # noqa: E402

SAIDA = sys.argv[1] if len(sys.argv) > 1 else "cartao.pdf"
VERDE, CREME, TINTA, OURO = "#1F3B2D", "#F4EFE6", "#22201C", "#C9A45C"

p = Peca(SAIDA, 9, 5, material="cartao", distancia_m=0.4, marcas_corte=True, titulo="Cartão — exemplo")
u = p.area_util

# ---- frente: marca centralizada sobre cor chapada ----
p.fundo(VERDE)
nome = p.texto("Ateliê Folha", "Gloock-Regular", 4.5, 2.55, cap=0.62, cor_texto=CREME, alinhar="centro",
               ancora="meio", nome="marca", fundo=VERDE)
p.linha(3.9, nome.y0 - 0.35, 5.1, nome.y0 - 0.35, OURO, 0.03)
p.texto("PAISAGISMO & JARDINS", "WorkSans-Regular", 4.5, nome.y0 - 0.75, pt=6.5, cor_texto=OURO, tracking=0.06,
        alinhar="centro", ancora="topo", nome="segmento", fundo=VERDE)

# ---- verso: contatos à esquerda, QR à direita ----
p.nova_pagina()
p.fundo(CREME)
p.texto("Marina Duarte", "WorkSans-Bold", u.x0, u.y1, pt=10, cor_texto=TINTA, ancora="topo", nome="pessoa", fundo=CREME)
p.texto("Paisagista · CREA 123456/SP", "WorkSans-Regular", u.x0, u.y1 - 0.62, pt=7, cor_texto=VERDE, ancora="topo",
        nome="cargo", fundo=CREME)
p.paragrafo("(11) 98765-4321\nmarina@ateliefolha.com.br\n@ateliefolha\nRua das Acácias, 120 · São Paulo",
            "WorkSans-Regular", u.x0, u.y0 + 1.75, largura=5.2, pt=7.2, entrelinha=1.45, cor_texto=TINTA, nome="contatos")
lado = 2.0
p.qrcode("https://ateliefolha.com.br", u.x1 - lado, u.y0, lado, cor_qr=TINTA, cor_fundo=CREME)

p.salvar()
