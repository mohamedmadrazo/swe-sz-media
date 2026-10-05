#!/usr/bin/env python3
"""Reconstruye la contraetiqueta real de Sharp Zombie (Tempranillo y Viura) con PIL a partir de los textos de la referencia del cliente.
Salida: textures/label_back.png (Tinto), textures/label_back_viura.png (Blanco). Tamaño 1536x3072 (etiqueta amarilla 2700 px + precinto blanco)."""
import os, random
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(HERE, 'fonts'); T = os.path.join(HERE, 'textures')
W, H, H2 = 1536, 2700, 372
YEL, RED, BLK, GRY = (255, 214, 0), (139, 0, 0), (12, 12, 12), (120, 120, 120)
def font(name, size):
    p = os.path.join(F, name)
    try:
        f = ImageFont.truetype(p, int(size))
        if 'Inter' in name:
            try: f.set_variation_by_name('Regular')
            except Exception: pass
        return f
    except Exception: return ImageFont.load_default()
def bold(size):
    f = font('Inter[opsz,wght].ttf', size)
    try: f.set_variation_by_axes([14, 700])
    except Exception: pass
    return f
def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines
def barcode(d, x, y, w, h, digits):
    rnd = random.Random(digits); px = x
    bars = [1, 1, 1] + [rnd.choice([1, 1, 2, 2, 3]) for _ in range(44)] + [1, 1, 1]
    unit = w / sum(bars) / 1.0
    for i, b in enumerate(bars):
        if i % 2 == 0: d.rectangle([px, y, px + b * unit * 0.55 + 1, y + h], fill=BLK)
        px += b * unit
    d.text((x + w / 2, y + h + 8), digits, font=font('Inter[opsz,wght].ttf', h * 0.32), fill=BLK, anchor='ma')
def qr(d, x, y, s, seed):
    rnd = random.Random(seed); n = 25; m = s / n
    for i in range(n):
        for j in range(n):
            fin = (i < 7 and j < 7) or (i < 7 and j >= n - 7) or (i >= n - 7 and j < 7)
            if fin:
                on = (i in (0, 6) or j in (0, 6) or (2 <= i <= 4 and 2 <= j <= 4)) if i < 7 and j < 7 else \
                     (i in (0, 6) or j in (n - 7, n - 1) or (2 <= i <= 4 and n - 5 <= j <= n - 3)) if i < 7 else \
                     (i in (n - 7, n - 1) or j in (0, 6) or (n - 5 <= i <= n - 3 and 2 <= j <= 4))
            else: on = rnd.random() < 0.45
            if on: d.rectangle([x + j * m, y + i * m, x + (j + 1) * m, y + (i + 1) * m], fill=BLK)
def build(varietal, colour, vol, ean, kcal, out):
    im = Image.new('RGB', (W, H + H2), (255, 255, 255)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H], fill=YEL)
    m = int(W * 0.06)
    # cabecera
    d.text((W / 2, H * 0.025), 'Sharp Zombie', font=font('UnifrakturMaguntia-Book.ttf', H * 0.075), fill=RED, anchor='ma')
    d.text((W / 2 + W * 0.21, H * 0.03), '®', font=font('Inter[opsz,wght].ttf', H * 0.02), fill=RED)
    d.text((m, H * 0.125), 'RIOJA', font=font('Anton-Regular.ttf', H * 0.06), fill=BLK)
    d.text((m, H * 0.195), 'Denominación de Origen Calificada', font=font('Inter[opsz,wght].ttf', H * 0.023), fill=BLK)
    d.text((m, H * 0.228), varietal, font=bold(H * 0.03), fill=BLK)
    # sello DOCa (gris) arriba derecha
    d.rectangle([W * 0.83, H * 0.125, W * 0.95, H * 0.195], outline=GRY, width=4, fill=(235, 220, 90))
    d.text((W * 0.89, H * 0.135), 'RIOJA', font=font('Anton-Regular.ttf', H * 0.026), fill=GRY, anchor='ma')
    d.text((W * 0.89, H * 0.168), 'D.O.Ca.', font=font('Inter[opsz,wght].ttf', H * 0.015), fill=GRY, anchor='ma')
    # cinta caution
    d.line([0, H * 0.272, W, H * 0.272], fill=BLK, width=5); d.line([0, H * 0.318, W, H * 0.318], fill=BLK, width=5)
    d.text((W / 2, H * 0.278), 'WINE        CAUTION : DEADLY GOOD WINE        CAUT', font=font('Anton-Regular.ttf', H * 0.03), fill=BLK, anchor='ma')
    # párrafo
    para = ("Sharp Zombie is a casual, flavorful wine made for easy enjoyment. Originally created for zombies—and preferred by the most sharply dressed in the zombie community—Sharp Zombie is now available for human consumption. It displays all the style and panache of the most elegant and relaxed members of the undead. Why stress? Simply enjoy. Caution: It's deadly good.")
    fp = font('Inter[opsz,wght].ttf', H * 0.0215); y = H * 0.345
    for ln in wrap(d, para, fp, W - 2 * m):
        d.text((m, y), ln, font=fp, fill=BLK); y += H * 0.0265
    # separador discontinuo
    yy = H * 0.625
    for x in range(m, W - m, 28): d.line([x, yy, x + 14, yy], fill=BLK, width=4)
    # SWE + productor
    d.rectangle([m, H * 0.645, m + W * 0.11, H * 0.695], fill=BLK)
    d.text((m + W * 0.055, H * 0.649), 'SWE', font=font('Anton-Regular.ttf', H * 0.036), fill=YEL, anchor='ma')
    fs = font('Inter[opsz,wght].ttf', H * 0.019)
    d.text((m + W * 0.13, H * 0.648), 'PRODUCED & BOTTLED FOR FINE WINES CO. SL', font=fs, fill=BLK)
    d.text((m + W * 0.13, H * 0.672), '26009 - ESPAÑA BY B.A. - AGONCILLO - R.E.N. 7216-LO', font=fs, fill=BLK)
    d.text((W * 0.62, H * 0.725), colour, font=font('Inter[opsz,wght].ttf', H * 0.024), fill=BLK, anchor='ma')
    d.text((W * 0.62, H * 0.755), 'PRODUCT OF SPAIN', font=bold(H * 0.026), fill=BLK, anchor='ma')
    # código de barras + QR
    barcode(d, m, H * 0.80, W * 0.36, H * 0.085, ean)
    d.text((W * 0.74, H * 0.795), 'INGREDIENTES', font=font('Inter[opsz,wght].ttf', H * 0.017), fill=BLK, anchor='ma')
    d.text((W * 0.74, H * 0.815), 'INFORMACIÓN NUTRICIONAL', font=font('Inter[opsz,wght].ttf', H * 0.017), fill=BLK, anchor='ma')
    qr(d, W * 0.69, H * 0.84, W * 0.10, ean)
    d.text((W * 0.74, H * 0.95), kcal, font=font('Inter[opsz,wght].ttf', H * 0.017), fill=BLK, anchor='ma')
    d.text((m, H * 0.905), '750 ML', font=font('Anton-Regular.ttf', H * 0.04), fill=BLK)
    d.text((m, H * 0.95), vol, font=font('Anton-Regular.ttf', H * 0.034), fill=BLK)
    d.text((m, H * 0.985 - H * 0.004), 'CONTIENE SULFITOS · CONTAINS SULPHITES', font=font('Inter[opsz,wght].ttf', H * 0.014), fill=BLK)
    # precinto Rioja (tira blanca)
    g = (90, 130, 50); y0 = H + 40
    d.rectangle([W * 0.08, y0, W * 0.40, H + H2 - 40], outline=(200, 200, 200), width=3)
    d.text((W * 0.24, y0 + 30), 'Rioja', font=font('UnifrakturMaguntia-Book.ttf', H2 * 0.3), fill=g, anchor='ma')
    d.text((W * 0.24, y0 + H2 * 0.55), 'Denominación de Origen Calificada', font=font('Inter[opsz,wght].ttf', H2 * 0.09), fill=g, anchor='ma')
    d.rectangle([W * 0.42, y0, W * 0.56, H + H2 - 40], fill=(150, 150, 150))
    d.text((W * 0.74, y0 + H2 * 0.18), 'UO Nº 246483', font=font('Inter[opsz,wght].ttf', H2 * 0.16), fill=BLK, anchor='ma')
    d.text((W * 0.74, y0 + H2 * 0.55), 'COSECHA', font=bold(H2 * 0.18), fill=BLK, anchor='ma')
    im.save(out, optimize=True); print(out, im.size)
os.makedirs(T, exist_ok=True)
build('Tempranillo', 'Red Spanish Wine', '13.0 %VOL', '8 436563 560149', 'E (100ml) 307kJ/73 kcal', os.path.join(T, 'label_back.png'))
build('Viura', 'White Spanish Wine', '12.0 %VOL', '8 436563 560156', 'E (100ml) 280kJ/68 kcal', os.path.join(T, 'label_back_viura.png'))
