"""retime_30s.py — convierte la escena de 15 s (v1_bottle_table.blend, 0-360 @24 fps) en la version de 30 s (v1_tokyo_30s.blend, 0-720).
1) Escala x2 el eje de frames (co.x, handle_left.x, handle_right.x) de TODAS las claves de TODAS las acciones (bpy.data.actions):
   objetos, datos de camara (lens / sensor_width), luces (energy) y node trees de materiales (GlowStrength / ZombieGlow / Washi).
   Blender 5.0: las acciones son "slotted" (sin Action.fcurves) -> se recorren action.layers -> strips -> channelbags -> fcurves.
2) Comprueba que el apagon del pendant queda en ~264-276 y el glow sube en ~320-380.
3) Overrides de camara SHOOT30 (en frames de 30 s; mismo mecanismo que los SHOOT de build_v1_scene.py), ver SHOOT30 mas abajo.
NO modifica v1_bottle_table.blend en disco (solo lo abre); guarda v1_tokyo_30s.blend.
Usage: python3 retime_30s.py [--src v1_bottle_table.blend] [--dst v1_tokyo_30s.blend] [--no-overrides]
"""
import bpy, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC, DST, OVERRIDES, SCALE = "v1_bottle_table.blend", "v1_tokyo_30s.blend", True, 2.0
args = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
for i, a in enumerate(args):
    if a == "--src": SRC = args[i+1]
    if a == "--dst": DST = args[i+1]
    if a == "--no-overrides": OVERRIDES = False
bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, SRC))
scn = bpy.context.scene
assert scn.frame_end == 360, f"la escena fuente no es la de 15 s (frame_end={scn.frame_end})"

def fcurves_of(action):
    """Todas las fcurves de una accion, tanto legacy (action.fcurves) como slotted (Blender 4.4+/5.0)."""
    fcs = getattr(action, "fcurves", None)
    if fcs is not None and len(fcs): return list(fcs)
    out = []
    for ly in action.layers:
        for st in ly.strips:
            for cb in st.channelbags: out.extend(cb.fcurves)
    return out

# ---------- 1) escala x2 ----------
n_keys = n_fc = 0
for act in bpy.data.actions:
    for fc in fcurves_of(act):
        for kp in fc.keyframe_points:
            kp.co.x *= SCALE; kp.handle_left.x *= SCALE; kp.handle_right.x *= SCALE; n_keys += 1
        fc.update(); n_fc += 1
    if act.use_frame_range: act.frame_start *= SCALE; act.frame_end *= SCALE
# NLA / marcadores (no hay en esta escena, pero por si acaso)
for idb in list(bpy.data.objects) + list(bpy.data.cameras) + list(bpy.data.lights) + [m.node_tree for m in bpy.data.materials if m.node_tree]:
    ad = getattr(idb, "animation_data", None)
    if ad and ad.nla_tracks:
        for tr in ad.nla_tracks:
            for st in tr.strips: st.frame_start *= SCALE; st.frame_end *= SCALE; print(f"[WARN] NLA strip escalado: {idb.name}/{st.name}")
for mk in scn.timeline_markers: mk.frame = int(round(mk.frame * SCALE))
scn.frame_start, scn.frame_end, scn.render.fps = 0, 720, 24
scn.frame_current = 0
print(f"[RETIME] {len(bpy.data.actions)} acciones, {n_fc} fcurves, {n_keys} claves x{SCALE:g}; frame range {scn.frame_start}-{scn.frame_end} @ {scn.render.fps} fps")

# ---------- 2) comprobaciones ----------
def find_fc(action, data_path, index=0):
    for fc in fcurves_of(action):
        if fc.data_path == data_path and fc.array_index == index: return fc
    raise KeyError(f"{action.name}: {data_path}[{index}]")
pend = find_fc(bpy.data.lights["Pendant"].animation_data.action, "energy")
pk = [int(round(k.co.x)) for k in pend.keyframe_points]
print(f"[CHECK] apagon pendant: claves energy en frames {pk} -> " + ", ".join(f"f{f}={pend.evaluate(f):.0f}W" for f in (262, 264, 270, 276, 278)))
assert pk == [264, 276], "el apagon no quedo en 264-276"
glow = find_fc(bpy.data.materials["SZ_Etiqueta_Frontal"].node_tree.animation_data.action, 'nodes["GlowStrength"].outputs[0].default_value')
gk = [(int(round(k.co.x)), round(k.co.y, 2)) for k in glow.keyframe_points]
rising = [f for f in range(300, 400) if glow.evaluate(f) > 0.05]
print(f"[CHECK] glow etiqueta: claves {gk}; >0 desde f{rising[0]} hasta f{rising[-1]}+ (pico 1 en f{max(range(312, 352), key=glow.evaluate)}, pico 2 en f{max(range(352, 400), key=glow.evaluate)})")
assert 312 <= rising[0] <= 330 and glow.evaluate(336) > 5.0, "el glow no sube en ~320-380"
zg = find_fc(bpy.data.materials["Zombie_1_Cutout_Mat"].node_tree.animation_data.action, 'nodes["ZombieGlow"].outputs[0].default_value')
print(f"[CHECK] ZombieGlow zombie_1: claves en {[int(round(k.co.x)) for k in zg.keyframe_points]}")
cam = bpy.data.objects["SZ_Camara"]; TGT = bpy.data.objects["CamTarget"]
cam_act = cam.animation_data.action; tgt_act = TGT.animation_data.action
print(f"[CHECK] claves camara (loc.x): {[int(round(k.co.x)) for k in find_fc(cam_act, 'location').keyframe_points]}")
print(f"[CHECK] claves sensor_width: {[(int(round(k.co.x)), k.co.y, k.interpolation) for k in find_fc(cam_act, 'sensor_width').keyframe_points]}")

# ---------- 3) overrides SHOOT30 ----------
# Razon (ver docs/video1_bible.md 'Version 30 s' y las comprobaciones de encuadre de renders_tests30/):
#  A) Fase iluminada 0-263: con sensor 36 (9:16 -> 20 mm horizontales) a 35 mm la pareja sentada sale de cuadro al avanzar el travelling
#     y la puerta de la cocina (x=2.0) nunca entra. Sensor 56 (como el fix de 64 de S5-S6), travelling mas corto (termina en -1.4,-2.4)
#     y paneo a la derecha 204-240 siguiendo la salida de Ren/Aya hasta la puerta; CORTE DURO en 264 al push-in original (S3).
#  B) Insert EE6 516-540 (sombra de Ren en la puerta): la camara a nivel de mesa de S5 mira a la botella (24 deg de FOV horizontal) y la
#     puerta queda 35 deg fuera. Corte a un plano desde la esquina delantera-izquierda de la mesa hacia +X: zombies en primer termino
#     (limbo), botella a la derecha y el hueco de la puerta con la sombra cruzando; vuelta al plano original en 541.
#  C) Final 648-720: el pull-back original (-0.3,-0.8) a 50 mm deja fuera al gato que asoma en (-0.55,-0.08). Pull-back en el eje de la
#     mirada hasta (-1.1,-0.9,0.95) a 50 mm, alcanzado en 684 (hold 1.5 s): copa cercana con los zombies en el centro, botella y copa lejana
#     a la derecha, gato en primer termino izquierda, luna arriba-izquierda.
SHOOT30_SENSOR = [(0, 56.0), (263, 56.0), (264, 36.0)]                      # (406, 36) y (408, 64) ya vienen escalados del fix S5-S6
SHOOT30_CAM = [  # (frame, cam loc, look_at, lens)  -- None = conservar el valor original evaluado en ese frame
    (192, (-1.4, -2.4, 1.35), (-0.1, 0.4, 0.92), 35), (204, (-1.4, -2.4, 1.35), (-0.1, 0.4, 0.92), 35),
    (240, (-1.4, -2.4, 1.35), (0.6, 0.5, 1.0), 35), (263, (-1.4, -2.4, 1.35), (0.6, 0.5, 1.0), 35),
    (515, None, None, None), (516, (-0.6, -0.3, 0.80), (1.0, 0.3, 0.9), 50), (540, (-0.6, -0.3, 0.80), (1.0, 0.3, 0.9), 50), (541, None, None, None),
    (684, (-1.1, -0.9, 0.95), (-0.15, 0.15, 0.8), 50), (720, (-1.1, -0.9, 0.95), (-0.15, 0.15, 0.8), 50)]
SHOOT30_DROP = [696]  # claves del pull-back de 15 s (348x2) que sustituye el override C (la de 720 se sobreescribe)

def drop_keys(fc, frames):
    for kp in [k for k in fc.keyframe_points if int(round(k.co.x)) in frames]: fc.keyframe_points.remove(kp)
    fc.update()
if OVERRIDES:
    cam_fcs = {("location", i): find_fc(cam_act, "location", i) for i in range(3)}; cam_fcs["lens"] = find_fc(cam_act, "lens")
    tgt_fcs = {i: find_fc(tgt_act, "location", i) for i in range(3)}
    # valores originales en los frames 'None' ANTES de tocar nada
    keep = {f: ([cam_fcs[("location", i)].evaluate(f) for i in range(3)], [tgt_fcs[i].evaluate(f) for i in range(3)], cam_fcs["lens"].evaluate(f))
            for f, loc, look, lens in SHOOT30_CAM if loc is None}
    for fc in list(cam_fcs.values()) + list(tgt_fcs.values()): drop_keys(fc, SHOOT30_DROP)
    for f, loc, look, lens in SHOOT30_CAM:
        if loc is None: loc, look, lens = keep[f]
        cam.location = loc; cam.keyframe_insert("location", frame=f); TGT.location = look; TGT.keyframe_insert("location", frame=f)
        cam.data.lens = lens; cam.data.keyframe_insert("lens", frame=f)
    for f, sw in SHOOT30_SENSOR: cam.data.sensor_width = sw; cam.data.keyframe_insert("sensor_width", frame=f)
    for kp in find_fc(cam_act, "sensor_width").keyframe_points: kp.interpolation = 'CONSTANT'
    print(f"[SHOOT30] overrides aplicados: {len(SHOOT30_CAM)} claves cam/target/lens, sensor {[(f, s) for f, s in SHOOT30_SENSOR]}")
    print(f"[CHECK] claves camara (loc.x) tras overrides: {[int(round(k.co.x)) for k in find_fc(cam_act, 'location').keyframe_points]}")
scn.frame_set(0)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, DST))
print(f"[DONE] guardado {DST}")
