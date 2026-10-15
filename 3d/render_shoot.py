# Rodaje S5-S6 (driving video para Genjutsu): frames 204-360 paso 1 a 540x960, CYCLES CPU, 12 samples + denoise.
# Abre v1_bottle_table.blend (construido por build_v1_scene.py --cutouts) y escribe renders_shoot/fNNN.png.
# Usage: python3 render_shoot.py [--start 204] [--end 360] [--step 1] [--samples 12] [--skip-existing]
#        [--blend v1_bottle_table.blend] [--out renders_shoot]           (version 30 s: --blend v1_tokyo_30s.blend --out renders_shoot30)
#        [--frames 0,60,150] [--res 270x480] [--no-denoise] [--prefix f] [--pad 3]   (stills de encuadre: --frames ignora start/end/step)
import bpy, os, sys, time
start, end, step, samples, skip = 204, 360, 1, 12, False
blend, out_dir, frames_list, res, denoise, prefix, pad = 'v1_bottle_table.blend', 'renders_shoot', None, (540, 960), True, 'f', 3
for i, a in enumerate(sys.argv):
    if a == "--start": start = int(sys.argv[i+1])
    if a == "--end": end = int(sys.argv[i+1])
    if a == "--step": step = int(sys.argv[i+1])
    if a == "--samples": samples = int(sys.argv[i+1])
    if a == "--skip-existing": skip = True
    if a == "--blend": blend = sys.argv[i+1]
    if a == "--out": out_dir = sys.argv[i+1]
    if a == "--frames": frames_list = [int(x) for x in sys.argv[i+1].split(",")]
    if a == "--res": res = tuple(int(x) for x in sys.argv[i+1].lower().split("x"))
    if a == "--no-denoise": denoise = False
    if a == "--prefix": prefix = sys.argv[i+1]
    if a == "--pad": pad = int(sys.argv[i+1])
here = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(here, blend))
scn = bpy.context.scene
scn.render.engine = "CYCLES"; scn.cycles.device = 'CPU'; scn.cycles.samples = samples; scn.cycles.use_denoising = denoise
try: scn.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
scn.render.resolution_x, scn.render.resolution_y = res; scn.render.resolution_percentage = 100
scn.render.image_settings.file_format = 'PNG'; scn.render.film_transparent = False
if scn.camera is None: scn.camera = bpy.data.objects.get('SZ_Camara')
out = os.path.join(here, out_dir); os.makedirs(out, exist_ok=True)
frames = frames_list if frames_list else list(range(start, end + 1, step)); t_all = time.time()
print(f"[START] {blend} frames {frames[0]}-{frames[-1]} ({len(frames)}) samples {samples} {res[0]}x{res[1]} denoise={denoise} -> {out}", flush=True)
for n, f in enumerate(frames):
    path = os.path.join(out, f'{prefix}{f:0{pad}d}.png')
    if skip and os.path.exists(path): print(f'[FRAME] {f} skip', flush=True); continue
    scn.frame_set(f); scn.render.filepath = path; t = time.time(); bpy.ops.render.render(write_still=True)
    dt = time.time() - t; el = time.time() - t_all; eta = (len(frames) - n - 1) * el / (n + 1)
    print(f'[FRAME] {f} {dt:.1f}s ({n+1}/{len(frames)}, elapsed {el/60:.1f} min, eta {eta/60:.1f} min)', flush=True)
print(f'[DONE] {len(frames)} frames in {(time.time()-t_all)/60:.1f} min', flush=True)
