# Previz animada local (bpy): frames 0-360 paso 2 (12 fps efectivos) a 360x640, CYCLES CPU.
import bpy, os, sys
samples, step = 12, 2
for i, a in enumerate(sys.argv):
    if a == "--samples": samples = int(sys.argv[i+1])
    if a == "--step": step = int(sys.argv[i+1])
here = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(here, 'v1_bottle_table.blend'))
scn = bpy.context.scene
scn.render.engine = "CYCLES"; scn.cycles.device = 'CPU'; scn.cycles.samples = samples; scn.cycles.use_denoising = True
try: scn.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
scn.render.resolution_x, scn.render.resolution_y = 360, 640; scn.render.resolution_percentage = 100
scn.render.image_settings.file_format = 'PNG'
if scn.camera is None: scn.camera = bpy.data.objects.get('SZ_Camara')
out = os.path.join(here, 'renders_anim'); os.makedirs(out, exist_ok=True)
for f in range(0, 361, step):
    scn.frame_set(f)
    scn.render.filepath = os.path.join(out, f'f{f:03d}.png')
    bpy.ops.render.render(write_still=True)
    print(f'[FRAME] {f}', flush=True)
print('[DONE]', flush=True)
