# Rodaje S5-S6 (driving video para Genjutsu): frames 204-360 paso 1 a 540x960, CYCLES CPU, 12 samples + denoise.
# Abre v1_bottle_table.blend (construido por build_v1_scene.py --cutouts) y escribe renders_shoot/fNNN.png.
# Usage: python3 render_shoot.py [--start 204] [--end 360] [--step 1] [--samples 12] [--skip-existing]
import bpy, os, sys, time
start, end, step, samples, skip = 204, 360, 1, 12, False
for i, a in enumerate(sys.argv):
    if a == "--start": start = int(sys.argv[i+1])
    if a == "--end": end = int(sys.argv[i+1])
    if a == "--step": step = int(sys.argv[i+1])
    if a == "--samples": samples = int(sys.argv[i+1])
    if a == "--skip-existing": skip = True
here = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(here, 'v1_bottle_table.blend'))
scn = bpy.context.scene
scn.render.engine = "CYCLES"; scn.cycles.device = 'CPU'; scn.cycles.samples = samples; scn.cycles.use_denoising = True
try: scn.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
scn.render.resolution_x, scn.render.resolution_y = 540, 960; scn.render.resolution_percentage = 100
scn.render.image_settings.file_format = 'PNG'; scn.render.film_transparent = False
if scn.camera is None: scn.camera = bpy.data.objects.get('SZ_Camara')
out = os.path.join(here, 'renders_shoot'); os.makedirs(out, exist_ok=True)
frames = list(range(start, end + 1, step)); t_all = time.time()
print(f"[START] frames {start}-{end} step {step} samples {samples} -> {out}", flush=True)
for n, f in enumerate(frames):
    path = os.path.join(out, f'f{f:03d}.png')
    if skip and os.path.exists(path): print(f'[FRAME] {f} skip', flush=True); continue
    scn.frame_set(f); scn.render.filepath = path; t = time.time(); bpy.ops.render.render(write_still=True)
    dt = time.time() - t; el = time.time() - t_all; eta = (len(frames) - n - 1) * el / (n + 1)
    print(f'[FRAME] {f} {dt:.1f}s ({n+1}/{len(frames)}, elapsed {el/60:.1f} min, eta {eta/60:.1f} min)', flush=True)
print(f'[DONE] {len(frames)} frames in {(time.time()-t_all)/60:.1f} min', flush=True)
