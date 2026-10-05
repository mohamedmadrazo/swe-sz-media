"""add_people_30s.py — anade a v1_tokyo_30s.blend (version 30 s, 0-720 @24 fps) los recortes (billboards imagen+alpha) de Aya, Ren y el gato,
la sombra de Ren (EE6, primitivas negras) que cruza el hueco de la puerta de la cocina, abre ese hueco en Wall_Right (+ suelo y pared de
cocina iluminada detras) y oculta para render los proxies legacy (Cat + hijos, Aya_Proxy/Ren_Proxy + hijos).
Idempotente: antes de crear borra todo objeto/mesh/material/imagen cuyo nombre empiece por "People_" y reposiciona Wall_Right.
PNG esperados en --people-dir (por defecto textures/people/): aya_seated.png (1.25 m, silla incluida), aya_standing.png (1.62 m),
ren_seated.png (1.32 m), ren_standing.png (1.76 m), cat_walking.png (0.30 m); RGBA con la figura recortada sobre alpha.
La altura se mide sobre el bbox del alpha (pies = borde inferior del bbox) y la anchura sale de la proporcion del PNG.
Si falta alguno se genera un PLACEHOLDER (silueta gris oscuro semitransparente, Pillow) en textures/people_placeholder/ y se avisa en consola.
Orientacion: los billboards miran a camara girando solo en Z (LOCKED_TRACK, como los zombies). Aya sentada mira a +X, Ren sentado a -X,
el resto a +X (sentido de la marcha). Se asume que cada PNG esta dibujado mirando a la derecha (+X); si un PNG real mira a la izquierda,
declararlo con --facing nombre=left (p.ej. --facing ren_seated=left) y el script no lo espejara.
Usage: python3 add_people_30s.py [--people-dir DIR] [--blend v1_tokyo_30s.blend] [--out v1_tokyo_30s.blend] [--facing a=left,b=right]
"""
import bpy, bmesh, math, os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PEOPLE_DIR, PH_DIR = os.path.join(HERE, "textures", "people"), os.path.join(HERE, "textures", "people_placeholder")
BLEND = OUT = "v1_tokyo_30s.blend"; FACING = {}
args = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
for i, a in enumerate(args):
    if a == "--people-dir": PEOPLE_DIR = os.path.abspath(args[i+1])
    if a == "--blend": BLEND = args[i+1]
    if a == "--out": OUT = args[i+1]
    if a == "--facing":
        for kv in args[i+1].split(","):
            k, v = kv.split("="); FACING[k.strip()] = -1 if v.strip().lower() in ("left", "l", "-x") else 1
# nombre -> (altura m, direccion deseada: +1 = mira a +X / derecha de camara, -1 = mira a -X)
FIGS = {"aya_seated": (1.25, 1), "aya_standing": (1.62, 1), "ren_seated": (1.32, -1), "ren_standing": (1.76, 1), "cat_walking": (0.30, 1)}
FPS = 24

# ---------- placeholders ----------
def placeholder(name):
    """Silueta gris oscuro semitransparente sobre alpha, mirando a la derecha. Devuelve la ruta del PNG."""
    os.makedirs(PH_DIR, exist_ok=True); path = os.path.join(PH_DIR, name + ".png")
    C = (40, 40, 46, 205)
    if name == "cat_walking":
        C = (88, 88, 96, 215)  # algo mas claro que las personas para que lea con luz de luna en la fase oscura (648-708)
        im = Image.new("RGBA", (1024, 512), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse((250, 180, 760, 400), fill=C); d.ellipse((700, 110, 900, 300), fill=C)                  # cuerpo, cabeza
        d.polygon([(730, 130), (770, 40), (800, 140)], fill=C); d.polygon([(830, 120), (880, 40), (890, 150)], fill=C)  # orejas
        for x in (300, 380, 620, 700): d.rectangle((x, 360, x + 55, 480), fill=C)                           # patas
        d.line([(270, 250), (150, 120), (90, 60)], fill=C, width=45)                                        # cola
    elif name.endswith("_seated"):
        im = Image.new("RGBA", (768, 1024), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        CH = (60, 44, 32, 230)                                                                               # silla (madera)
        d.rectangle((120, 560, 170, 990), fill=CH); d.rectangle((120, 250, 165, 600), fill=CH)             # pata trasera + respaldo
        d.rectangle((120, 560, 470, 600), fill=CH); d.rectangle((430, 600, 470, 990), fill=CH)             # asiento + pata delantera
        d.ellipse((330, 80, 530, 280), fill=C)                                                              # cabeza
        d.polygon([(200, 300), (480, 300), (470, 580), (190, 580)], fill=C)                                 # torso
        d.polygon([(190, 540), (560, 540), (590, 650), (200, 650)], fill=C)                                 # muslos
        d.rectangle((520, 640, 600, 980), fill=C); d.rectangle((420, 640, 500, 980), fill=C)               # piernas
        d.polygon([(470, 330), (560, 330), (640, 560), (590, 560)], fill=C)                                 # brazo adelante
        d.ellipse((560, 940, 680, 1000), fill=C)                                                            # pie
    else:  # standing, perfil hacia la derecha
        im = Image.new("RGBA", (512, 1024), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse((215, 20, 375, 180), fill=C)                                                              # cabeza
        d.polygon([(200, 190), (380, 190), (400, 520), (190, 520)], fill=C)                                 # torso
        d.polygon([(195, 500), (400, 500), (420, 760), (330, 760), (300, 600), (270, 760), (180, 760)], fill=C)  # caderas/muslos
        d.rectangle((180, 740, 265, 990), fill=C); d.rectangle([(330, 740), (420, 990)], fill=C)           # piernas
        d.polygon([(360, 210), (420, 210), (450, 500), (400, 500)], fill=C)                                 # brazo
        d.ellipse((330, 950, 480, 1005), fill=C)                                                            # pie adelantado
    im.save(path); return path

def figure_png(name):
    real = os.path.join(PEOPLE_DIR, name + ".png")
    if os.path.exists(real): print(f"[PNG] {name}: {real}"); return real, False
    p = placeholder(name); print(f"[PLACEHOLDER] {name}: no existe {real} -> usando placeholder {p}"); return p, True

# ---------- escena ----------
bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, BLEND))
scn = bpy.context.scene
assert scn.frame_end == 720, f"{BLEND} no es la escena de 30 s (frame_end={scn.frame_end}); ejecuta antes retime_30s.py"
cam = bpy.data.objects["SZ_Camara"]
# idempotencia: borrar todo lo People_*
for o in [o for o in bpy.data.objects if o.name.startswith("People_")]: bpy.data.objects.remove(o, do_unlink=True)
for coll, _ in ((bpy.data.meshes, 0), (bpy.data.materials, 0), (bpy.data.images, 0), (bpy.data.lights, 0), (bpy.data.actions, 0)):
    for x in [x for x in coll if x.name.startswith("People_")]: coll.remove(x)

def add(name, prim, loc, scale=(1, 1, 1), rot=(0, 0, 0), m=None, **kw):
    getattr(bpy.ops.mesh, f"primitive_{prim}_add")(location=loc, **kw)
    o = bpy.context.active_object; o.name = name; o.data.name = name + "_Mesh"; o.scale = scale; o.rotation_euler = rot
    if m: o.data.materials.append(m)
    return o

def cutout_material(name, path):
    """Imagen RGBA -> Base Color + Alpha (sin emision), alpha hashed para sombras/render."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    img = nt.nodes.new("ShaderNodeTexImage"); im = bpy.data.images.load(path); im.name = name + "_Img"; img.image = im
    im.colorspace_settings.name = 'sRGB'; img.extension = 'CLIP'
    nt.links.new(img.outputs["Color"], b.inputs["Base Color"]); nt.links.new(img.outputs["Alpha"], b.inputs["Alpha"])
    b.inputs["Roughness"].default_value = 0.9; b.inputs["Emission Strength"].default_value = 0.0
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.1
    for attr, val in (("surface_render_method", 'DITHERED'), ("blend_method", 'HASHED'), ("shadow_method", 'HASHED')):
        try: setattr(m, attr, val)
        except Exception: pass
    return m

def billboard(name, path, height_m, mirror=False):
    """Plano vertical que mira a -Y, pies de la figura (borde inferior del bbox del alpha) en z=0 local, centrado en el bbox.
    Escala: height_m = altura del bbox del alpha; la anchura sale de la proporcion del PNG."""
    im = Image.open(path).convert("RGBA"); W, H = im.size; bb = im.getchannel("A").getbbox() or (0, 0, W, H)
    S = height_m / (bb[3] - bb[1]); w, h = W * S, H * S; z0 = -(H - bb[3]) * S; xo = -((bb[0] + bb[2]) / 2 - W / 2) * S
    bm = bmesh.new(); vs = [bm.verts.new(p) for p in ((xo - w/2, 0, z0), (xo + w/2, 0, z0), (xo + w/2, 0, z0 + h), (xo - w/2, 0, z0 + h))]
    face = bm.faces.new(vs); uvl = bm.loops.layers.uv.new("UVMap")
    uvs = ((1, 0), (0, 0), (0, 1), (1, 1)) if mirror else ((0, 0), (1, 0), (1, 1), (0, 1))
    for loop, uvc in zip(face.loops, uvs): loop[uvl].uv = uvc
    me = bpy.data.meshes.new(name + "_Mesh"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); scn.collection.objects.link(o)
    o.data.materials.append(cutout_material(name + "_Mat", path))
    c = o.constraints.new('LOCKED_TRACK'); c.target = cam; c.track_axis = 'TRACK_NEGATIVE_Y'; c.lock_axis = 'LOCK_Z'
    return o

# ---------- animacion ----------
def key(o, f, loc=None, rot=None):
    if loc is not None: o.location = loc; o.keyframe_insert("location", frame=f)
    if rot is not None: o.rotation_euler = rot; o.keyframe_insert("rotation_euler", frame=f)
def visible(o, ranges):
    """hide_render/hide_viewport keyframeados (CONSTANT): visible solo dentro de los rangos [a, b] (inclusive)."""
    marks = {0: True}
    for a, b in ranges: marks[a] = False; marks[b + 1] = True
    for a, _ in ranges: marks[a] = False
    for f, hidden in sorted(marks.items()):
        o.hide_render = hidden; o.hide_viewport = hidden; o.keyframe_insert("hide_render", frame=f); o.keyframe_insert("hide_viewport", frame=f)
    for fc in [fc for ly in o.animation_data.action.layers for st in ly.strips for cb in st.channelbags for fc in cb.fcurves]:
        if fc.data_path.startswith("hide_"):
            for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'
def laugh(o, x, y, f0, f1, period=20, dz=0.01, tilt=2.0):
    """Vaiven de risa: +-dz en Z y +-tilt grados de inclinacion lateral (rot Y local sobrevive al LOCKED_TRACK en Z)."""
    for f in list(range(f0, f1, 5)) + [f1]:
        ph = 2 * math.pi * (f - f0) / period
        key(o, f, loc=(x, y, dz * math.sin(ph)), rot=(0, math.radians(tilt) * math.sin(ph + 0.9), 0))
def walk(o, path, step=6, bob=0.012, lean=2.5):
    """path = [(frame, x, y), ...]; claves cada `step` frames con bob vertical y balanceo lateral alternos (sin bob en tramos parados)."""
    f0, f1 = path[0][0], path[-1][0]; n = 0
    for f in list(range(f0, f1, step)) + [f1]:
        for (fa, xa, ya), (fb, xb, yb) in zip(path, path[1:]):
            if fa <= f <= fb:
                t = (f - fa) / (fb - fa) if fb > fa else 0; x, y = xa + (xb - xa) * t, ya + (yb - ya) * t; moving = (xa, ya) != (xb, yb); break
        s = 1 if n % 2 else -1; n += 1
        key(o, f, loc=(x, y, bob * (0.5 + 0.5 * s) if moving else 0.0), rot=(0, math.radians(lean) * s if moving else 0, 0))

made, ph_used = {}, []
for name, (h, want) in FIGS.items():
    path, is_ph = figure_png(name); native = FACING.get(name, 1)
    made[name] = billboard("People_" + name, path, h, mirror=(native != want))
    if is_ph: ph_used.append(name)
A_S, A_T, R_S, R_T, CAT = (made[k] for k in ("aya_seated", "aya_standing", "ren_seated", "ren_standing", "cat_walking"))
# Aya: sentada silla izquierda 0-200 (risa 0-192), de pie 200-270 saliendo por detras de la mesa hacia la puerta (x=2.0, y=0.6)
laugh(A_S, -0.98, 0.4, 0, 192); key(A_S, 200, loc=(-0.98, 0.4, 0), rot=(0, 0, 0)); visible(A_S, [(0, 199)])
key(A_T, 200, loc=(-0.98, 0.4, 0)); walk(A_T, [(204, -0.98, 0.4), (216, -0.9, 1.0), (248, 1.5, 1.0), (258, 2.0, 0.6), (270, 2.7, 0.6)]); visible(A_T, [(200, 270)])
# Ren: sentado silla derecha 0-192 (mira a -X), de pie 192-258
laugh(R_S, 0.98, 0.4, 0, 186); key(R_S, 192, loc=(0.98, 0.4, 0), rot=(0, 0, 0)); visible(R_S, [(0, 191)])
key(R_T, 192, loc=(0.98, 0.4, 0)); walk(R_T, [(196, 0.98, 0.4), (218, 1.6, 0.7), (240, 2.0, 0.6), (258, 2.7, 0.6)]); visible(R_T, [(192, 258)])
# Gato: cruce en primer termino y=-0.9 (120-192, pausa 150-162) + asoma por el borde cercano de la mesa (648-708)
walk(CAT, [(120, -1.6, -0.9), (150, -0.35, -0.9), (162, -0.35, -0.9), (192, 1.6, -0.9)], step=4, bob=0.015, lean=3.0)
for f, z in ((648, 0.30), (664, 0.60), (690, 0.60), (708, 0.30)): key(CAT, f, loc=(-0.55, -0.08, z), rot=(0, 0, 0))  # asomo: cabeza y hombros sobre el borde (top gato 0.90 m vs mesa 0.72)
visible(CAT, [(120, 192), (648, 708)])
# ---------- hueco de la puerta de la cocina (x=2.0, y=0.6, ancho 0.9, alto 2.1) + cocina iluminada detras ----------
M_wall = bpy.data.materials["Wall_Plaster"]; M_floor = bpy.data.materials["Oak_Floor"]
wr = bpy.data.objects["Wall_Right"]; wr.location = (2.0, -1.125, 1.35); wr.scale = (0.05, 1.275, 1.35)          # y -2.4..0.15
add("People_Wall_Right_Far", "cube", (2.0, 1.125, 1.35), (0.05, 0.075, 1.35), m=M_wall)                         # y 1.05..1.2
add("People_Door_Lintel", "cube", (2.0, 0.6, 2.4), (0.05, 0.45, 0.3), m=M_wall)                                   # z 2.1..2.7
add("People_Kitchen_Floor", "plane", (2.6, 0.6, 0.0), (0.6, 1.0, 1), m=M_floor)
M_kw = bpy.data.materials.new("People_Kitchen_Glow"); M_kw.use_nodes = True; bk = M_kw.node_tree.nodes["Principled BSDF"]
bk.inputs["Base Color"].default_value = (0.9, 0.78, 0.6, 1.0); bk.inputs["Emission Color"].default_value = (1.0, 0.82, 0.55, 1.0); bk.inputs["Emission Strength"].default_value = 0.5
add("People_Kitchen_Wall", "cube", (3.2, 0.6, 1.35), (0.05, 1.2, 1.35), m=M_kw)
Ld = bpy.data.lights.new("People_Kitchen_Light", 'POINT'); Ld.energy = 80; Ld.color = (1.0, 0.85, 0.6); Ld.shadow_soft_size = 0.3
kl = bpy.data.objects.new("People_Kitchen_Light", Ld); scn.collection.objects.link(kl); kl.location = (2.7, 0.6, 2.2)
# ---------- sombra de Ren (EE6): cilindro + esfera, negro puro sin especular, 1.76 m; cruza la puerta 516-540 ----------
M_sh = bpy.data.materials.new("People_Shadow_Black"); M_sh.use_nodes = True; bs = M_sh.node_tree.nodes["Principled BSDF"]
bs.inputs["Base Color"].default_value = (0, 0, 0, 1); bs.inputs["Roughness"].default_value = 1.0; bs.inputs["Metallic"].default_value = 0.0
for k in ("Specular IOR Level", "Specular", "Coat Weight", "Sheen Weight"):
    if k in bs.inputs: bs.inputs[k].default_value = 0.0
bm = bmesh.new()
for v in bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.16, radius2=0.14, depth=1.5)["verts"]: v.co.z += 0.75   # cuerpo z 0..1.5
for v in bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=0.13)["verts"]: v.co.z += 1.63                         # cabeza, top 1.76
me = bpy.data.meshes.new("People_RenShadow_Mesh"); bm.to_mesh(me); bm.free()
SH = bpy.data.objects.new("People_RenShadow", me); scn.collection.objects.link(SH); SH.data.materials.append(M_sh)
key(SH, 516, loc=(2.05, 0.1, 0)); key(SH, 540, loc=(2.05, 1.1, 0)); visible(SH, [(516, 540)])
# ---------- proxies legacy fuera del render (gato de primitivas, capsulas de Aya/Ren; no hay sillas de proxy en la escena) ----------
for n in ("Cat", "Cat_Body", "Cat_Head", "Cat_Tail", "Aya_Proxy", "Aya_Proxy_Body", "Aya_Proxy_Head", "Ren_Proxy", "Ren_Proxy_Body", "Ren_Proxy_Head"):
    o = bpy.data.objects.get(n)
    if o: o.hide_render = True
scn.frame_set(0)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, OUT))
print(f"[PEOPLE] billboards: {[o.name for o in made.values()]} + People_RenShadow, puerta abierta en Wall_Right, proxies legacy ocultos")
if ph_used: print(f"[PLACEHOLDER] figuras con placeholder: {ph_used} -> cuando existan los PNG reales en {PEOPLE_DIR}, re-ejecutar este script")
print(f"[DONE] guardado {OUT}")
