# Turntable de la botella Sharp Zombie (escena local bpy): 36 vistas x 2 pasadas (lit / glow), CYCLES CPU.
import bpy, math, os, sys
samples = 16
for i, a in enumerate(sys.argv):
    if a == "--samples": samples = int(sys.argv[i+1])
here = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(here, 'v1_bottle_table.blend'))
scn = bpy.context.scene
scn.render.engine = "CYCLES"; scn.cycles.device = 'CPU'; scn.cycles.samples = samples; scn.cycles.use_denoising = True
try: scn.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
scn.render.resolution_x, scn.render.resolution_y = 540, 960; scn.render.resolution_percentage = 100
scn.render.image_settings.file_format = 'PNG'
# ocultar personajes/gato/zombies para el turntable de producto
for o in scn.objects:
    if o.name.startswith(('Zombie', 'Hand', 'Cat', 'Aya', 'Ren', 'Mano', 'Gato')):
        o.hide_render = True
tgt = bpy.data.objects.new('TurnTarget', None); scn.collection.objects.link(tgt); tgt.location = (0.15, 0.10, 0.86)
cd = bpy.data.cameras.new('TurnCamData'); cd.lens = 50
cam = bpy.data.objects.new('TurnCam', cd); scn.collection.objects.link(cam)
c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
scn.camera = cam
out = os.path.join(here, 'renders_turntable'); os.makedirs(out, exist_ok=True)
N, R, H = 36, 0.60, 0.95
for name, frame in [('lit', 60), ('glow', 190)]:
    scn.frame_set(frame)
    for i in range(N):
        a = math.radians(i * 360 / N)
        cam.location = (0.15 + R * math.sin(a), 0.10 - R * math.cos(a), H)
        scn.render.filepath = os.path.join(out, f'{name}_{i:02d}.png')
        bpy.ops.render.render(write_still=True)
        print(f'[FRAME] {name} {i}', flush=True)
print('[DONE]', flush=True)
