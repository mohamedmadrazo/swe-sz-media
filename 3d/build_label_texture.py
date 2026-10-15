"""Build the front-label texture + glow mask for the Sharp Zombie bottle (local, 0 credits).
Source A (preferred): textures/label_front_packshot.png  (perspective crop of the 2K packshot, when downloadable)
Source B (fallback):  ../poster/gen_0e5ffd25.webp  (lit label frame) + ../img/producto_real.webp (real glow outlines)
Outputs: textures/label_front.png (1536x2048), textures/label_glow_mask.png (same size), textures/label_debug.png
"""
import os, sys
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageFont
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(HERE, "textures"); os.makedirs(T, exist_ok=True)
W, H = 1536, 2048
src = os.path.join(T, "label_front_packshot.png")
if os.path.exists(src):
    base = Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS); origin = "packshot"
else:
    im = Image.open(os.path.join(HERE, "..", "poster", "gen_0e5ffd25.webp")).convert("RGB")
    a = np.asarray(im).astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    yellow = (r > 150) & (g > 120) & (b < 110) & (r - b > 90)
    ys, xs = np.where(yellow)
    # keep the dense central blob (label), ignore stray pixels
    y0, y1 = np.percentile(ys, 0.5), np.percentile(ys, 99.5); x0, x1 = np.percentile(xs, 0.5), np.percentile(xs, 99.5)
    box = (int(x0) - 4, int(y0) - 6, int(x1) + 4, int(y1) + 6)
    base = im.crop(box).resize((W, H), Image.LANCZOS); origin = f"poster crop {box}"
base = ImageOps.autocontrast(base, cutoff=0.5)
base.save(os.path.join(T, "label_front.png"))
# glow mask: dark silhouettes in the lower figure band (between the RIOJA block and the bottom stripes)
a = np.asarray(base).astype(int); lum = (a[..., 0] * 299 + a[..., 1] * 587 + a[..., 2] * 114) // 1000
mask = np.zeros((H, W), dtype=np.uint8)
band = slice(int(H * 0.60), int(H * 0.885))
dark = (lum[band] < 95) & (a[band, :, 0] < 120)  # exclude dark-red blackletter (R stays higher)
mask[band] = (dark * 255).astype(np.uint8)
m = Image.fromarray(mask).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(3))  # close gaps
# outline-only version (thin luminous edge like the real glow ink)
edge = np.asarray(m).astype(int); inner = np.asarray(m.filter(ImageFilter.MinFilter(9))).astype(int)
outline = np.clip(edge - inner, 0, 255).astype(np.uint8)
Image.fromarray(outline).filter(ImageFilter.GaussianBlur(1.2)).save(os.path.join(T, "label_glow_mask.png"))
m.save(os.path.join(T, "label_silhouettes_fill.png"))
# debug composite
dbg = base.copy(); ov = Image.new("RGB", (W, H), (57, 255, 20)); dbg.paste(ov, (0, 0), Image.fromarray(outline))
dbg.resize((384, 512)).save(os.path.join(T, "label_debug.png"))
cov = float((np.asarray(m) > 0).mean())
print(f"origin={origin} size={W}x{H} silhouette_coverage={cov:.4f}")
