#!/usr/bin/env python3
"""Couverture de l'article sur les certificats à 100 jours (1000x420, pour dev.to).

Rejouer :  ~/.venv-docgen/bin/python tools/covers/certificates-100-days-march-2027.py
Requiert fontTools + brotli dans le venv (pour lire fonts/inter-*.woff2) et Pillow.
Le visuel EST l'argument de l'article : la fenêtre de validité qui rétrécit.
"""
import os, tempfile
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_TMP = tempfile.mkdtemp(prefix="inter-")
for _w in ("400", "600", "700"):
    _f = TTFont(os.path.join(REPO, "fonts", f"inter-{_w}.woff2"))
    _f.flavor = None
    _f.save(os.path.join(_TMP, f"inter-{_w}.ttf"))
S = _TMP
OUT = os.path.join(REPO, "covers", "certificates-100-days-march-2027.png")

W, H = 1000, 420
CANVAS, INK, BODY, MUTE = "#101010", "#f2f2f2", "#bdbdbd", "#8b949e"
ACCENT, HAIR, SOFT = "#00d992", "#3d3a39", "#1a1a1a"

def f(w, s): return ImageFont.truetype(f"{S}/inter-{w}.ttf", s)

img = Image.new("RGB", (W, H), CANVAS)
d = ImageDraw.Draw(img)
PAD = 56

d.text((PAD, 38),  "Certificates drop to",   font=f("700", 42), fill=INK)
d.text((PAD, 86),  "100 days in March 2027", font=f("700", 42), fill=INK)
d.text((PAD, 142), "The renewals nobody owns are what break.", font=f("400", 19), fill=BODY)
d.line([(PAD, 184), (W - PAD, 184)], fill=HAIR, width=1)

rows = [("2020", 398, None), ("March 2026", 200, "in force"),
        ("March 2027", 100, "next"), ("March 2029", 47, None)]
LABEL_W, NUM_W = 150, 110
TRACK = W - PAD * 2 - LABEL_W - NUM_W
PXD = TRACK / 398
y, STEP = 206, 43
x0 = PAD + LABEL_W

# axe de départ des barres
d.line([(x0 - 14, 202), (x0 - 14, y + STEP * 3 + 22)], fill=HAIR, width=1)

for label, days, note in rows:
    hot = note == "next"
    if hot:  # marqueur d'accent à gauche de la rangée vive
        d.rectangle([PAD - 14, y - 2, PAD - 11, y + 24], fill=ACCENT)
    d.text((PAD, y + 2), label, font=f("600" if hot else "400", 15),
           fill=INK if hot else MUTE)
    w = max(7, int(days * PXD))
    d.rounded_rectangle([x0, y, x0 + w, y + 22], radius=3,
                        fill=ACCENT if hot else SOFT,
                        outline=None if hot else HAIR, width=1)
    d.text((x0 + w + 14, y + 3), f"{days} days", font=f("600", 16),
           fill=INK if hot else MUTE)
    if note and not hot:
        tw = d.textlength(f"{days} days", font=f("600", 16))
        d.text((x0 + w + 14 + tw + 10, y + 4), note, font=f("400", 14), fill=HAIR)
    y += STEP

foot = "CA/Browser Forum ballot SC-081v3"
d.text((PAD, H - 44), foot, font=f("400", 14), fill=HAIR)
site = "wistonlestin.com"
d.text((W - PAD - d.textlength(site, font=f("600", 14)), H - 44),
       site, font=f("600", 14), fill=MUTE)
img.save(OUT, optimize=True)
print("écrit:", OUT, img.size)
