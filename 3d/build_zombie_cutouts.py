"""Cut the 5 label silhouettes (3 walkers, 1 crouched, 1 little hand) out of textures/label_silhouettes_fill.png
as square RGBA billboards for the Blender scene (local, 0 credits, PIL + numpy only — no OpenCV / scipy).
Outputs (textures/):
  zombie_01.png … zombie_05.png          RGBA, matte black silhouette + thin lime (#39FF14) outline (dilation − mask)
  zombie_01_outline.png … _05_outline.png L, outline-only mask (white = glow) to drive emission in the material
  zombies.json                           order left→right, label bbox, canvas geometry, relative heights, flags
Usage: python3 build_zombie_cutouts.py [--canvas 1024] [--outline 0.035]
"""
import os, sys, json
from collections import deque
from PIL import Image, ImageFilter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(HERE, "textures")
CANVAS = 1024; OUTLINE_FRAC = 0.035; FIT = 0.76; FEET_V = 0.12; LIME = (0x39, 0xFF, 0x14)
args = sys.argv[1:]
for i, a in enumerate(args):
    if a == "--canvas": CANVAS = int(args[i+1])
    if a == "--outline": OUTLINE_FRAC = float(args[i+1])

fill = np.asarray(Image.open(os.path.join(T, "label_silhouettes_fill.png")).convert("L")) > 127
H, W = fill.shape
LABEL_H_M = 0.11; PX_M = LABEL_H_M / H  # label zone is 0.11 m tall → metres per pixel (v1_beats.json)

# ---------- connected components (4-neighbour BFS over the mask) ----------
def components(mask):
    lab = np.zeros(mask.shape, dtype=np.int32); comps = []; n = 0
    ys, xs = np.nonzero(mask)
    for y, x in zip(ys, xs):
        if lab[y, x]: continue
        n += 1; lab[y, x] = n; q = deque([(y, x)]); pts = []
        while q:
            cy, cx = q.popleft(); pts.append((cy, cx))
            for ny, nx in ((cy-1, cx), (cy+1, cx), (cy, cx-1), (cy, cx+1)):
                if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = n; q.append((ny, nx))
        p = np.array(pts); y0, x0 = p.min(0); y1, x1 = p.max(0)
        comps.append({"id": n, "area": len(pts), "bbox": [int(x0), int(y0), int(x1), int(y1)]})
    return lab, comps

lab, comps = components(fill)
def keep(c):
    x0, y0, x1, y1 = c["bbox"]; w, h = x1 - x0 + 1, y1 - y0 + 1
    if c["area"] < 1500 or h < 80: return False            # text remnants / specks
    if x1 >= W - 2 and w < 0.08 * W: return False           # bar on the right label edge
    if h < 0.25 * w and y1 > H * 0.86: return False         # bottom stripe remnants
    if y0 < H * 0.61 and h < 150: return False              # 'Calificada' text line just above the figures
    return True
figs = sorted([c for c in comps if keep(c)], key=lambda c: c["bbox"][0])
print(f"components={len(comps)} kept={len(figs)}")
for c in figs: print("  ", c["id"], "area", c["area"], "bbox", c["bbox"])
if len(figs) != 5:
    print("WARNING: expected 5 figures, got", len(figs)); figs = figs[:5]

# ---------- classify by order left→right (walker, walker, walker, crouch, hand) ----------
KIND = ["walker", "walker", "walker", "crouch", "hand"]; NAMES = ["walker_a", "walker_b", "walker_c", "crouch", "hand"]

# ---------- circular dilation via FFT convolution with a disk ----------
def dilate_disk(mask01, r):
    k = 2 * r + 1; yy, xx = np.mgrid[-r:r+1, -r:r+1]; disk = ((xx*xx + yy*yy) <= r*r).astype(np.float32)
    Hh, Ww = mask01.shape; pad = np.zeros((Hh + k, Ww + k), np.float32); pad[:Hh, :Ww] = mask01
    kern = np.zeros_like(pad); kern[:k, :k] = disk; kern = np.roll(kern, (-r, -r), axis=(0, 1))
    conv = np.fft.irfft2(np.fft.rfft2(pad) * np.fft.rfft2(kern), s=pad.shape)
    return (conv[:Hh, :Ww] > 0.5)

meta = {"source": "label_silhouettes_fill.png", "source_size": [W, H], "label_zone_height_m": LABEL_H_M, "canvas": CANVAS,
        "outline_frac": OUTLINE_FRAC, "fit_frac": FIT, "feet_v": FEET_V, "lime": "#39FF14", "order": "left→right on the label", "figures": []}
S = CANVAS; r_out = max(2, int(round(OUTLINE_FRAC * S)))
for i, c in enumerate(figs):
    x0, y0, x1, y1 = c["bbox"]; w, h = x1 - x0 + 1, y1 - y0 + 1
    crop = (lab[y0:y1+1, x0:x1+1] == c["id"]).astype(np.uint8) * 255
    clipped_left = x0 <= 1 or (x0 < 0.03 * W and w < 0.2 * h)  # cut or heavily foreshortened by the label edge / bottle curvature
    # fit the figure into FIT*S (longest side), bottom edge at FEET_V from the canvas bottom, centred horizontally
    sc = FIT * S / max(w, h); fw, fh = max(1, int(round(w * sc))), max(1, int(round(h * sc)))
    fig = Image.fromarray(crop).resize((fw, fh), Image.LANCZOS)
    can = Image.new("L", (S, S), 0); ox = (S - fw) // 2; oy = int(round(S * (1 - FEET_V))) - fh
    can.paste(fig, (ox, oy))
    soft = np.asarray(can).astype(np.float32) / 255.0            # anti-aliased fill
    hard = soft > 0.5
    dil = dilate_disk(hard.astype(np.float32), r_out)
    outline = np.clip(dil.astype(np.float32) - soft, 0, 1)
    outline = np.asarray(Image.fromarray((outline * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32) / 255.0
    outline = np.clip(outline - soft, 0, 1)                      # keep the body matte black
    alpha = np.clip(soft + outline, 0, 1)
    rgb = np.zeros((S, S, 3), np.float32)
    for ch in range(3): rgb[..., ch] = LIME[ch] / 255.0 * outline  # body stays black (0,0,0)
    rgba = np.dstack([rgb, alpha]); Image.fromarray((rgba * 255 + 0.5).astype(np.uint8), "RGBA").save(os.path.join(T, f"zombie_{i+1:02d}.png"))
    Image.fromarray((outline * 255 + 0.5).astype(np.uint8), "L").save(os.path.join(T, f"zombie_{i+1:02d}_outline.png"))
    meta["figures"].append({
        "index": i + 1, "file": f"zombie_{i+1:02d}.png", "outline_file": f"zombie_{i+1:02d}_outline.png", "name": NAMES[i], "kind": KIND[i],
        "label_bbox_px": [x0, y0, x1, y1], "label_size_px": [w, h], "label_height_m": round(h * PX_M, 5), "label_width_m": round(w * PX_M, 5),
        "label_center_u": round((x0 + x1) / 2 / W, 4), "label_center_v": round(1 - (y0 + y1) / 2 / H, 4),
        "canvas_bbox_px": [ox, oy, ox + fw - 1, oy + fh - 1], "figure_height_frac": round(fh / S, 4), "figure_width_frac": round(fw / S, 4),
        "feet_v": FEET_V, "height_rel_to_tallest": None, "area_px": c["area"], "clipped_left_edge": bool(clipped_left),
    })
tallest = max(f["label_size_px"][1] for f in meta["figures"])
for f in meta["figures"]: f["height_rel_to_tallest"] = round(f["label_size_px"][1] / tallest, 4)
for f in meta["figures"]:
    if f["clipped_left_edge"]: f["scene_stand_in"] = "zombie_03 (walker_c) mirrored in UV — walker_a is a foreshortened sliver at the label edge"
json.dump(meta, open(os.path.join(T, "zombies.json"), "w"), indent=2, ensure_ascii=False)
# contact sheet for a quick visual check
sheet = Image.new("RGBA", (S // 4 * 5, S // 4), (90, 90, 60, 255))
for i in range(len(figs)): sheet.paste(Image.open(os.path.join(T, f"zombie_{i+1:02d}.png")).resize((S // 4, S // 4)), (i * S // 4, 0))
sheet.save(os.path.join(T, "zombies_sheet.png"))
for f in meta["figures"]: print(f'{f["file"]} {f["name"]:9s} label {f["label_size_px"]} px = {f["label_height_m"]*100:.2f} cm tall  canvas h_frac {f["figure_height_frac"]}  clipped={f["clipped_left_edge"]}')
print("[DONE]")
