#!/usr/bin/env python3
"""Couverture de l article « 100% partout est un drapeau rouge » (1000x420, pour dev.to).

Rejouer :  ~/.venv-docgen/bin/python tools/covers/lab-metrics-red-flag.py
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
OUT = os.path.join(REPO, "covers", "lab-metrics-red-flag.png")

W, H = 1000, 420
CANVAS, INK, BODY, MUTE = "#101010", "#f2f2f2", "#bdbdbd", "#8b949e"
ACCENT, HAIR, SOFT = "#00d992", "#3d3a39", "#1a1a1a"

def f(w, s): return ImageFont.truetype(f"{S}/inter-{w}.ttf", s)

img = Image.new("RGB", (W, H), CANVAS)
d = ImageDraw.Draw(img)
PAD = 56

d.text((PAD, 32), "Perfect scores on every row.",   font=f("700", 40), fill=INK)
d.text((PAD, 78), "The honest number was 0.0%.",    font=f("700", 40), fill=INK)
d.text((PAD, 130), "What the metric measured was the naivety of the dataset.",
       font=f("400", 18), fill=BODY)
d.line([(PAD, 172), (W - PAD, 172)], fill=HAIR, width=1)

COLS = [("Detector", PAD, "left"), ("F1", 470, "right"),
        ("Precision", 610, "right"), ("Recall", 740, "right"), ("FP rate", 888, "right")]
rows = [("Phishing URLs",            "100%", "100%", "100%", "0%",   False),
        ("Prompt abuse",             "100%", "100%", "100%", "0%",   False),
        ("Identity anomalies",       "100%", "100%", "100%", "0%",   False),
        ("Network  ·  Isolation Forest", "0.0%", "0.0%", "0.0%", "0.0%", True)]

def put(txt, x, align, font, fill):
    w = d.textlength(txt, font=font)
    d.text((x - w if align == "right" else x, put.y), txt, font=font, fill=fill)

put.y = 192
for name, x, align in COLS:
    put(name, x, align, f("400", 13), HAIR)

y = 218
for name, f1, pr, rc, fp, hot in rows:
    put.y = y + 3
    if hot:
        d.rectangle([PAD - 14, y, PAD - 11, y + 24], fill=ACCENT)
    col = INK if hot else MUTE
    put(name, PAD, "left", f("600" if hot else "400", 16), col)
    for val, (_, x, align) in zip((f1, pr, rc, fp), COLS[1:]):
        put(val, x, align, f("600", 17), ACCENT if hot else MUTE)
    if not hot:
        d.line([(PAD, y + 33), (W - PAD, y + 33)], fill=SOFT, width=1)
    y += 40

d.text((PAD, H - 44), "Synthetic fixtures: the exam where the questions are the answers",
       font=f("400", 14), fill=HAIR)
site = "wistonlestin.com"
d.text((W - PAD - d.textlength(site, font=f("600", 14)), H - 44),
       site, font=f("600", 14), fill=MUTE)
img.save(OUT, optimize=True)
print("écrit:", OUT, img.size)
