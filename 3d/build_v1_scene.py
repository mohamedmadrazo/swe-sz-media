"""Local Blender (bpy) scene for Sharp Zombie V1 previz: bottle with real label texture + glow, glasses, table,
camera path and choreography from v1_beats.json. Renders with CYCLES (CPU) only — Eevee needs a GPU context.
Usage: python3 build_v1_scene.py [--frames f1,f2,...] [--samples N] [--no-render] [--cutouts | --no-cutouts]
Outputs: v1_bottle_table.blend, v1_bottle_table.glb, renders/previz_fNNN.png
--cutouts (default): zombies/hand are label cut-out billboards (textures/zombie_NN.png from build_zombie_cutouts.py)
--no-cutouts: legacy capsule proxies.
"""
import bpy, bmesh, json, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(HERE, "textures"); R = os.path.join(HERE, "renders"); os.makedirs(R, exist_ok=True)
beats = json.load(open(os.path.join(HERE, "v1_beats.json")))
args = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
frames = [0, 72, 132, 170, 240, 300, 330, 360]; samples = 24; do_render = True; use_cutouts = True
for i, a in enumerate(args):
    if a == "--frames": frames = [int(x) for x in args[i+1].split(",")]
    if a == "--samples": samples = int(args[i+1])
    if a == "--no-render": do_render = False
    if a == "--cutouts": use_cutouts = True
    if a == "--no-cutouts": use_cutouts = False
ZJ = None
if use_cutouts:
    zj_path = os.path.join(T, "zombies.json")
    if os.path.exists(zj_path): ZJ = json.load(open(zj_path))
    else: print("zombies.json not found (run build_zombie_cutouts.py) -> falling back to capsule proxies"); use_cutouts = False
scn = bpy.context.scene
scn.render.engine = "CYCLES"; scn.cycles.device = 'CPU'; scn.cycles.samples = samples; scn.cycles.use_denoising = True
try: scn.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
scn.render.fps = beats["fps"]; scn.frame_start = beats["frame_start"]; scn.frame_end = beats["frame_end"]
scn.render.resolution_x, scn.render.resolution_y = 540, 960; scn.render.resolution_percentage = 100
scn.render.film_transparent = False
for o in list(scn.objects): bpy.data.objects.remove(o, do_unlink=True)
L = beats["layout"]

def mat(name, rgb, rough=0.6, emit=None, strength=0.0, alpha=1.0, metallic=0.0, transmission=0.0, ior=1.45):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1.0); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metallic
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1.0); b.inputs["Emission Strength"].default_value = strength
    for key in ("Transmission Weight", "Transmission"):
        if key in b.inputs and transmission: b.inputs[key].default_value = transmission; b.inputs["IOR"].default_value = ior; break
    if alpha < 1.0: b.inputs["Alpha"].default_value = alpha
    return m

def add(name, prim, loc, scale=(1,1,1), rot=(0,0,0), m=None, **kw):
    getattr(bpy.ops.mesh, f"primitive_{prim}_add")(location=loc, **kw)
    o = bpy.context.active_object; o.name = name; o.scale = scale; o.rotation_euler = rot
    if m: o.data.materials.append(m)
    return o
def empty(name, loc):
    e = bpy.data.objects.new(name, None); scn.collection.objects.link(e); e.location = loc; e.empty_display_size = 0.05; return e

# ---------- materials ----------
M_floor = mat("Oak_Floor", (0.55, 0.42, 0.28), 0.5); M_wall = mat("Wall_Plaster", (0.82, 0.80, 0.76), 0.9); M_walnut = mat("Walnut", (0.26, 0.15, 0.09), 0.45)
M_moon = mat("Moon", (0.9, 0.93, 1.0), 1.0, emit=(0.75, 0.85, 1.0), strength=12.0); M_sky = mat("Skyline", (0.02, 0.03, 0.08), 0.8, emit=(0.12, 0.2, 0.45), strength=0.25)
M_bottle = mat("SZ_Vidrio", (0.03, 0.008, 0.01), 0.08, transmission=0.35, ior=1.5); M_wineInside = mat("SZ_Vino", (0.3, 0.02, 0.05), 0.2, transmission=0.6, ior=1.34)
M_cap = mat("SZ_Capsula_Rosca", (0.02, 0.02, 0.02), 0.35, metallic=0.4); M_wineglass = mat("Copa_Vidrio", (1, 1, 1), 0.02, transmission=1.0, ior=1.5)
M_wine = mat("Copa_Vino", (0.3, 0.02, 0.05), 0.15, transmission=0.5, ior=1.34); M_ceramic = mat("Ceramica", (0.93, 0.9, 0.85), 0.5)
M_zombie = mat("Zombie_Glow", (0.0, 0.0, 0.0), 0.9, emit=(0.22, 1.0, 0.08), strength=0.0); M_cat = mat("Gato_Calico", (0.9, 0.6, 0.3), 0.8)
M_people = mat("Persona_Proxy", (0.6, 0.6, 0.65), 0.8); M_lamp = mat("Washi", (1.0, 0.9, 0.7), 0.9, emit=(1.0, 0.75, 0.4), strength=4.0)
# label material: texture + glow mask emission
M_label = bpy.data.materials.new("SZ_Etiqueta_Frontal"); M_label.use_nodes = True; nt = M_label.node_tree; b = nt.nodes["Principled BSDF"]
tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = bpy.data.images.load(os.path.join(T, "label_front.png")); tex.image.colorspace_settings.name = 'sRGB'
mask = nt.nodes.new("ShaderNodeTexImage"); mask.image = bpy.data.images.load(os.path.join(T, "label_glow_mask.png")); mask.image.colorspace_settings.name = 'Non-Color'
glow = nt.nodes.new("ShaderNodeValue"); glow.name = "GlowStrength"; glow.outputs[0].default_value = 0.0
mul = nt.nodes.new("ShaderNodeMath"); mul.operation = 'MULTIPLY'
nt.links.new(tex.outputs["Color"], b.inputs["Base Color"]); nt.links.new(mask.outputs["Color"], mul.inputs[0]); nt.links.new(glow.outputs[0], mul.inputs[1]); nt.links.new(mul.outputs[0], b.inputs["Emission Strength"])
b.inputs["Emission Color"].default_value = (0.22, 1.0, 0.08, 1.0); b.inputs["Roughness"].default_value = 0.55
for f, v in beats["glow"]["strength_keys"]:
    scn.frame_set(f); glow.outputs[0].default_value = v * 6.0; glow.outputs[0].keyframe_insert("default_value")
# dark-phase label base darkening handled by lighting

# ---------- room ----------
add("Floor", "plane", (0, 0.5, 0), (2.0, 3.0, 1), m=M_floor)
add("Wall_Left", "cube", (-2.0, 0.5, 1.35), (0.05, 3.0, 1.35), m=M_wall); add("Wall_Right", "cube", (2.0, -0.6, 1.35), (0.05, 1.8, 1.35), m=M_wall)
add("Skyline_Card", "plane", (0, 2.9, 1.2), (3.0, 1.3, 1), (math.radians(90), 0, 0), m=M_sky)
add("Moon", "circle", (L["moon"]["center"][0], 2.86, L["moon"]["center"][2]), (L["moon"]["radius"],)*2 + (1,), (math.radians(90), 0, 0), m=M_moon, fill_type='NGON')
add("Pendant_Shade", "uv_sphere", tuple(L["pendant"]["pos"]), (0.22, 0.22, 0.16), m=M_lamp)
tb = L["table"]; add("Table_Top", "cube", (tb["center"][0], tb["center"][1], tb["top_z"]-0.02), (tb["size"][0]/2, tb["size"][1]/2, 0.02), m=M_walnut)
for i, (x, y) in enumerate([(-0.6, 0.05), (0.6, 0.05), (-0.6, 0.75), (0.6, 0.75)]): add(f"Table_Leg_{i}", "cylinder", (x, y, 0.34), (0.025, 0.025, 0.34), m=M_walnut)
add("Plate_L", "cylinder", (-0.4, 0.4, 0.73), (0.11, 0.11, 0.008), m=M_ceramic); add("Plate_R", "cylinder", (0.4, 0.42, 0.73), (0.11, 0.11, 0.008), m=M_ceramic)
add("Edamame_Bowl", "cylinder", (0.05, 0.55, 0.745), (0.06, 0.06, 0.025), m=M_ceramic); add("Chopstick_Rest", "cube", (-0.05, -0.05, 0.728), (0.025, 0.008, 0.008), m=M_ceramic)
add("Chopstick_A", "cylinder", (-0.05, 0.02, 0.745), (0.003, 0.003, 0.11), (math.radians(80), 0, math.radians(10)), m=M_walnut)
# ---------- bottle (spin profile) ----------
BX, BY, BZ = L["bottle"]["pos"]; RB = L["bottle"]["radius"]
profile = [(0.0, 0.0), (RB*0.85, 0.0), (RB, 0.012), (RB, 0.200), (RB*0.92, 0.222), (0.0145, 0.262), (0.0135, 0.290), (0.0135, 0.300), (0.0, 0.300)]
bm = bmesh.new(); verts = [bm.verts.new((x, 0, z)) for x, z in profile]
bmesh.ops.spin(bm, geom=verts, cent=(0,0,0), axis=(0,0,1), dvec=(0,0,0), angle=2*math.pi, steps=64, use_duplicate=False)
bm.verts.ensure_lookup_table(); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
me = bpy.data.meshes.new("SZ_Botella_Mesh"); bm.to_mesh(me); bm.free(); bottle = bpy.data.objects.new("SZ_Botella", me); scn.collection.objects.link(bottle)
bottle.location = (BX, BY, BZ); bottle.data.materials.append(M_bottle)
for p in bottle.data.polygons: p.use_smooth = True
add("SZ_Tapon_Rosca", "cylinder", (BX, BY, BZ+0.306), (0.0145, 0.0145, 0.012), m=M_cap)
add("SZ_Vino_Interior", "cylinder", (BX, BY, BZ+0.10), (RB*0.93, RB*0.93, 0.095), m=M_wineInside)
add("SZ_Tapon_Suelto", "cylinder", tuple(L["screw_cap"]["pos"][:2]) + (BZ+0.01,), (0.015, 0.015, 0.01), m=M_cap)
# label: cylinder segment with UVs (arc 150 deg facing -Y)
lab_h = L["bottle"]["label_zone_height"]; lab_z0 = L["bottle"]["label_center_z"] - lab_h/2 - BZ; r = RB + 0.0006
bm = bmesh.new(); N = 24; ang0, ang1 = math.radians(-165), math.radians(-15)
rows = []
for j in range(2):
    row = []
    for i in range(N+1):
        a = ang0 + (ang1-ang0)*i/N; row.append(bm.verts.new((r*math.cos(a), r*math.sin(a), lab_z0 + j*lab_h)))
    rows.append(row)
uv = bm.loops.layers.uv.new("UVMap")
for i in range(N):
    f = bm.faces.new((rows[0][i], rows[0][i+1], rows[1][i+1], rows[1][i]))
    for loop in f.loops:
        idx = [rows[0][i], rows[0][i+1], rows[1][i+1], rows[1][i]].index(loop.vert)
        u = (i if idx in (0,3) else i+1)/N; v = 0.0 if idx in (0,1) else 1.0
        loop[uv].uv = (u, v)
me = bpy.data.meshes.new("SZ_Etiqueta_Mesh"); bm.to_mesh(me); bm.free(); label = bpy.data.objects.new("SZ_Etiqueta", me); scn.collection.objects.link(label)
label.location = (BX, BY, BZ); label.data.materials.append(M_label)
# ---------- back label (contraetiqueta real, textures/label_back.png: etiqueta 2700 px + precinto 372 px) ----------
if os.path.exists(os.path.join(T, "label_back.png")):
    M_back = bpy.data.materials.new("SZ_Contraetiqueta"); M_back.use_nodes = True; ntb = M_back.node_tree; bb = ntb.nodes["Principled BSDF"]
    texb = ntb.nodes.new("ShaderNodeTexImage"); texb.image = bpy.data.images.load(os.path.join(T, "label_back.png")); texb.image.colorspace_settings.name = 'sRGB'
    ntb.links.new(texb.outputs["Color"], bb.inputs["Base Color"]); bb.inputs["Roughness"].default_value = 0.55
    back_h = lab_h * 3072.0 / 2700.0; back_z0 = lab_z0 - lab_h * 372.0 / 2700.0
    bm = bmesh.new(); ang0b, ang1b = math.radians(15), math.radians(165); rows = []
    for j in range(2):
        row = []
        for i in range(N+1):
            a = ang0b + (ang1b-ang0b)*i/N; row.append(bm.verts.new((r*math.cos(a), r*math.sin(a), back_z0 + j*back_h)))
        rows.append(row)
    uvb = bm.loops.layers.uv.new("UVMap")
    for i in range(N):
        f = bm.faces.new((rows[0][i], rows[0][i+1], rows[1][i+1], rows[1][i]))
        for loop in f.loops:
            idx = [rows[0][i], rows[0][i+1], rows[1][i+1], rows[1][i]].index(loop.vert)
            u = (i if idx in (0,3) else i+1)/N; v = 0.0 if idx in (0,1) else 1.0
            loop[uvb].uv = (u, v)
    meb = bpy.data.meshes.new("SZ_Contraetiqueta_Mesh"); bm.to_mesh(meb); bm.free(); back = bpy.data.objects.new("SZ_Contraetiqueta", meb); scn.collection.objects.link(back)
    back.location = (BX, BY, BZ); back.data.materials.append(M_back)
# ---------- glasses ----------
def glass(name, x, y, fill):
    add(f"{name}_Base", "cylinder", (x, y, BZ+0.004), (0.035, 0.035, 0.004), m=M_wineglass)
    add(f"{name}_Stem", "cylinder", (x, y, BZ+0.05), (0.004, 0.004, 0.045), m=M_wineglass)
    add(f"{name}_Bowl", "cone", (x, y, BZ+0.15), (1,1,1), m=M_wineglass, radius1=0.028, radius2=0.045, depth=0.11)
    add(f"{name}_Wine", "cone", (x, y, BZ+0.095+0.055*fill*0.9), (1,1,1), m=M_wine, radius1=0.027, radius2=0.027+0.017*fill, depth=0.11*fill)
g1, g2 = L["glass_near"], L["glass_far"]; glass("Copa_Cerca", g1["pos"][0], g1["pos"][1], g1["fill"]); glass("Copa_Lejos", g2["pos"][0], g2["pos"][1], g2["fill"])
# ---------- characters ----------
ZGLOW = 4.0  # emission strength of the lime outline when ZombieGlow = 1
CUTOUT_PLANES = []
def cutout_material(name, fig):
    """Label cut-out: image RGBA -> base colour + alpha; outline mask x ZombieGlow -> lime emission."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    img = nt.nodes.new("ShaderNodeTexImage"); img.image = bpy.data.images.load(os.path.join(T, fig["file"])); img.image.colorspace_settings.name = 'sRGB'; img.extension = 'CLIP'
    ol = nt.nodes.new("ShaderNodeTexImage"); ol.image = bpy.data.images.load(os.path.join(T, fig["outline_file"])); ol.image.colorspace_settings.name = 'Non-Color'; ol.extension = 'CLIP'
    glow = nt.nodes.new("ShaderNodeValue"); glow.name = "ZombieGlow"; glow.label = "ZombieGlow"; glow.outputs[0].default_value = 0.0
    mul = nt.nodes.new("ShaderNodeMath"); mul.operation = 'MULTIPLY'
    nt.links.new(img.outputs["Color"], b.inputs["Base Color"]); nt.links.new(img.outputs["Alpha"], b.inputs["Alpha"])
    nt.links.new(ol.outputs["Color"], mul.inputs[0]); nt.links.new(glow.outputs[0], mul.inputs[1]); nt.links.new(mul.outputs[0], b.inputs["Emission Strength"])
    b.inputs["Emission Color"].default_value = (0.22, 1.0, 0.08, 1.0); b.inputs["Roughness"].default_value = 0.9
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.1
    for attr, val in (("surface_render_method", 'DITHERED'), ("blend_method", 'HASHED'), ("shadow_method", 'HASHED')):
        try: setattr(m, attr, val)
        except Exception: pass
    for f, v in beats["glow"]["strength_keys"]:  # 0 before frame 156, pulse 156-190, held at ZGLOW afterwards
        scn.frame_set(f); glow.outputs[0].default_value = v * ZGLOW; glow.outputs[0].keyframe_insert("default_value")
    return m
def billboard(name, fig, height_m, mirror=False):
    """Vertical square plane facing -Y, feet of the figure at local z=0 (so the empty = the feet, like the capsules)."""
    S = height_m / fig["figure_height_frac"]; z0 = -fig["feet_v"] * S
    bm = bmesh.new(); vs = [bm.verts.new(p) for p in ((-S/2, 0, z0), (S/2, 0, z0), (S/2, 0, z0+S), (-S/2, 0, z0+S))]
    face = bm.faces.new(vs); uvl = bm.loops.layers.uv.new("UVMap")
    uvs = ((1, 0), (0, 0), (0, 1), (1, 1)) if mirror else ((0, 0), (1, 0), (1, 1), (0, 1))
    for loop, uvc in zip(face.loops, uvs): loop[uvl].uv = uvc
    me = bpy.data.meshes.new(name + "_Mesh"); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); scn.collection.objects.link(o)
    o.data.materials.append(cutout_material(name + "_Mat", fig)); CUTOUT_PLANES.append(o); return o
def zombie(name, x, y, z, h=0.05, crouch=False, fig=None, mirror=False):
    e = empty(name, (x, y, z))
    if fig is not None:
        p = billboard(f"{name}_Cutout", fig, h, mirror); p.parent = e; return e
    parts = [add(f"{name}_Body", "cylinder", (0, 0, h*0.45), (0.0075, 0.0075, h*0.3 if not crouch else h*0.18), m=M_zombie),
             add(f"{name}_Head", "uv_sphere", (0, 0, h*0.85 if not crouch else h*0.5), (0.0085,)*3, m=M_zombie),
             add(f"{name}_ArmL", "cylinder", (-0.006, -0.012, h*0.62 if not crouch else h*0.35), (0.0025, 0.0025, 0.014), (math.radians(90), 0, 0), m=M_zombie),
             add(f"{name}_ArmR", "cylinder", (0.006, -0.012, h*0.62 if not crouch else h*0.35), (0.0025, 0.0025, 0.014), (math.radians(90), 0, 0), m=M_zombie)]
    for p in parts: p.parent = e
    return e
LY = BY - RB - 0.004
if use_cutouts:
    FIG = {f["name"]: f for f in ZJ["figures"]}
    # walker_a is a foreshortened sliver at the label edge -> Zombie_1 uses walker_c mirrored (see zombies.json scene_stand_in)
    Z = [zombie("Zombie_1", BX-0.022, LY, BZ+0.09, fig=FIG["walker_c"], mirror=True), zombie("Zombie_2", BX, LY, BZ+0.09, fig=FIG["walker_b"]),
         zombie("Zombie_3", BX+0.022, LY, BZ+0.09, fig=FIG["walker_c"])]
    ZC = zombie("Zombie_Crouch", BX+0.012, LY, BZ+0.055, h=0.03, fig=FIG["crouch"])
    HAND = empty("Hand", (BX-0.028, LY, BZ+0.055)); hb = billboard("Hand_Cutout", FIG["hand"], 0.02); hb.parent = HAND
else:
    Z = [zombie("Zombie_1", BX-0.022, LY, BZ+0.09), zombie("Zombie_2", BX, LY, BZ+0.09), zombie("Zombie_3", BX+0.022, LY, BZ+0.09)]
    ZC = zombie("Zombie_Crouch", BX+0.012, LY, BZ+0.055, crouch=True)
    HAND = empty("Hand", (BX-0.028, LY, BZ+0.055)); hb = add("Hand_Mesh", "cube", (0, 0, 0.006), (0.005, 0.004, 0.006), m=M_zombie); hb.parent = HAND
CAT = empty("Cat", (-2.0, -1.0, 0))
for p in (add("Cat_Body", "cube", (0, 0, 0.12), (0.20, 0.07, 0.10), m=M_cat), add("Cat_Head", "uv_sphere", (0.22, 0, 0.22), (0.07,)*3, m=M_cat), add("Cat_Tail", "cylinder", (-0.22, 0, 0.18), (0.015, 0.015, 0.05), (0, math.radians(40), 0), m=M_cat)): p.parent = CAT
AYA = empty("Aya_Proxy", (-0.98, 0.4, 0)); RENP = empty("Ren_Proxy", (0.98, 0.4, 0))
for e, h in ((AYA, 1.65), (RENP, 1.75)):
    for p in (add(f"{e.name}_Body", "cylinder", (0, 0, 0.44+(h-0.5)*0.5*0.55), (0.17, 0.17, (h-0.5)*0.5*0.55), m=M_people), add(f"{e.name}_Head", "uv_sphere", (0, 0, 0.44+(h-0.5)*0.55+0.12), (0.11, 0.11, 0.12), m=M_people)): p.parent = e
# ---------- lights ----------
def light(name, t, loc, energy, color=(1,1,1)):
    Ld = bpy.data.lights.new(name, t); Ld.energy = energy; Ld.color = color; o = bpy.data.objects.new(name, Ld); scn.collection.objects.link(o); o.location = loc; return o
lights = beats["lights"]
PEND = light("Pendant", 'POINT', tuple(lights["pendant"]["pos"]), 450, (1.0, 0.75, 0.45)); PEND.data.shadow_soft_size = 0.2
FLAMP = light("FloorLamp", 'POINT', tuple(lights["floor_lamp"]["pos"]), 160, (1.0, 0.75, 0.45))
KSPILL = light("Kitchen_Spill", 'SPOT', tuple(lights["kitchen_spill"]["pos"]), 80, (0.8, 0.9, 1.0)); KSPILL.data.spot_size = math.radians(80); KSPILL.rotation_euler = (math.radians(60), 0, math.radians(90))
MOON = light("Moon_Sun", 'SUN', (0.3, 2.4, 2.2), 0.6, (0.6, 0.72, 1.0)); MOON.rotation_euler = (math.radians(-55), math.radians(5), math.radians(10)); MOON.data.angle = math.radians(1.0)
for Lo in (PEND, FLAMP, KSPILL):
    f0, f1 = lights["pendant"]["off_frames"]; e0 = Lo.data.energy
    scn.frame_set(f0); Lo.data.energy = e0; Lo.data.keyframe_insert("energy"); scn.frame_set(f1); Lo.data.energy = 0.0; Lo.data.keyframe_insert("energy")
s = M_lamp.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]; scn.frame_set(132); s.keyframe_insert("default_value"); scn.frame_set(138); s.default_value = 0.0; s.keyframe_insert("default_value")
s = M_zombie.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
for f, v in beats["glow"]["strength_keys"]: scn.frame_set(f); s.default_value = v * 3.0; s.keyframe_insert("default_value")
scn.world = scn.world or bpy.data.worlds.new("World"); scn.world.use_nodes = True
wb = scn.world.node_tree.nodes.get("Background"); wb.inputs[0].default_value = (0.01, 0.012, 0.03, 1.0); wb.inputs[1].default_value = 0.6
# ---------- camera ----------
cam = bpy.data.objects.new("SZ_Camara", bpy.data.cameras.new("SZ_Camara")); scn.collection.objects.link(cam); scn.camera = cam; cam.data.sensor_width = 36; cam.data.clip_start = 0.01
TGT = empty("CamTarget", (0, 0.6, 0.95)); c = cam.constraints.new('TRACK_TO'); c.target = TGT; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
for k in beats["camera_keys"]:
    scn.frame_set(k["frame"]); cam.location = k["loc"]; cam.keyframe_insert("location"); TGT.location = k["look_at"]; TGT.keyframe_insert("location"); cam.data.lens = k["lens"]; cam.data.keyframe_insert("lens")
# cut-out billboards: keep them facing the camera (rotate only about their own Z, so the parents' wobble tilt survives)
for o in CUTOUT_PLANES:
    c = o.constraints.new('LOCKED_TRACK'); c.target = cam; c.track_axis = 'TRACK_NEGATIVE_Y'; c.lock_axis = 'LOCK_Z'
if use_cutouts:
    # S5-S6 shoot framing fix (frames 204-360 only; S1-S4 untouched): the 36 mm sensor on a 9:16 frame gives a ~13 deg horizontal
    # FOV at 85 mm and the figures were out of frame most of the time. Wider sensor from the S4->S5 hard cut + extra keys following
    # the choreography (bottle base -> chopsticks party -> hold on the freeze -> climb/drop -> wide final with both glasses + bottle).
    SHOOT_SENSOR = [(203, 36.0), (204, 64.0)]
    SHOOT_KEYS = [(228, (-0.02, -0.36, 0.78), (0.10, 0.07, 0.75), 85), (244, (-0.14, -0.40, 0.79), (-0.02, 0.02, 0.75), 85),
                  (258, (-0.24, -0.41, 0.79), (-0.07, 0.0, 0.74), 85), (276, (-0.40, -0.42, 0.81), (-0.08, 0.0, 0.75), 85),
                  (284, (-0.40, -0.42, 0.81), (-0.08, 0.0, 0.75), 85), (348, (-0.3, -0.8, 0.98), (0.06, 0.15, 0.82), 50), (360, (-0.3, -0.8, 0.98), (0.06, 0.15, 0.82), 50)]
    for f, sw in SHOOT_SENSOR: scn.frame_set(f); cam.data.sensor_width = sw; cam.data.keyframe_insert("sensor_width")
    act = cam.data.animation_data.action
    fcs = list(act.fcurves) if getattr(act, "fcurves", None) else [fc for ly in act.layers for st in ly.strips for cb in st.channelbags for fc in cb.fcurves]
    for fc in fcs:
        if fc.data_path == "sensor_width":
            for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'
    for f, loc, look, lens in SHOOT_KEYS:
        scn.frame_set(f); cam.location = loc; cam.keyframe_insert("location"); TGT.location = look; TGT.keyframe_insert("location"); cam.data.lens = lens; cam.data.keyframe_insert("lens")
# ---------- choreography ----------
def key(e, f, loc=None, rot=None, scale=None):
    scn.frame_set(f)
    if loc is not None: e.location = loc; e.keyframe_insert("location")
    if rot is not None: e.rotation_euler = rot; e.keyframe_insert("rotation_euler")
    if scale is not None: e.scale = scale; e.keyframe_insert("scale")
Tz = BZ
for i, (e, dx) in enumerate(zip(Z, (-0.022, 0.0, 0.022))):
    x0 = BX + dx; lag = i * 6
    key(e, 204 + lag, loc=(x0, LY, BZ+0.09)); key(e, 214 + lag, loc=(x0, LY-0.03, Tz))
    key(e, 252, loc=(-0.11 + dx, 0.02, Tz)); key(e, 262, loc=(-0.07 + dx, -0.02, Tz - 0.004)); key(e, 270, loc=(-0.03 + dx, -0.06, Tz)); key(e, 284, loc=(-0.03 + dx, -0.06, Tz))
    sp = 1.0 if use_cutouts else 0.6  # cut-out billboards are wider than the capsules: keep the three readable side by side on the stem / in the bowl
    key(e, 288, loc=(-0.20 + dx*sp, 0.11, Tz)); key(e, 306, loc=(-0.20 + dx*sp, 0.11, Tz+0.10)); key(e, 324, loc=(-0.20 + dx*sp, 0.12, Tz+0.205))
    sp = 1.0 if use_cutouts else 0.7
    key(e, 336, loc=(-0.20 + dx*sp, 0.15, Tz+0.13)); key(e, 348, loc=(-0.20 + dx*sp, 0.15, Tz+0.135), rot=(0, math.radians(25), 0)); key(e, 360, loc=(-0.20 + dx*sp, 0.15, Tz+0.13), rot=(0, math.radians(-15), 0))
    for f in (212, 222, 232, 242): key(e, f + lag, rot=(0, 0, math.radians(20 if (f//10) % 2 else -20)))
key(ZC, 228, loc=(BX+0.012, LY, BZ+0.055)); key(ZC, 240, loc=(BX+0.012, LY-0.03, Tz)); key(ZC, 262, loc=(-0.04, 0.0, Tz)); key(ZC, 288, loc=(0.42, 0.14, Tz)); key(ZC, 324, loc=(0.42, 0.15, Tz+0.205)); key(ZC, 336, loc=(0.45, 0.2, Tz+0.15)); key(ZC, 360, loc=(0.45, 0.2, Tz+0.15), rot=(0, math.radians(90), 0) if use_cutouts else (math.radians(90), 0, 0))  # billboard floats on its side instead of edge-on
if use_cutouts:  # extra life on the cut-outs themselves (children): side lean while walking, finger-walk rock on the hand
    for i, e in enumerate(Z):
        p = e.children[0]; lag = i * 6
        for n, f in enumerate(range(204 + lag, 253, 6)): key(p, f, rot=(0, math.radians(8 if n % 2 else -8), 0))
        key(p, 258, rot=(0, 0, 0))
    hp = HAND.children[0]
    for n, f in enumerate(range(210, 253, 5)): key(hp, f, rot=(0, math.radians(10 if n % 2 else -10), 0))
    key(hp, 258, rot=(0, 0, 0))
key(HAND, 210, loc=(BX-0.028, LY, BZ+0.055)); key(HAND, 222, loc=(BX-0.03, LY-0.03, Tz)); key(HAND, 252, loc=(-0.08, 0.03, Tz)); key(HAND, 288, loc=(-0.17, 0.10, Tz)); key(HAND, 324, loc=(-0.165, 0.11, Tz+0.21)); key(HAND, 360, loc=(-0.165, 0.11, Tz+0.21))
key(CAT, 0, loc=(-2.2, -1.0, 0), scale=(0,0,0)); key(CAT, 59, scale=(0,0,0)); key(CAT, 60, loc=(-2.2, -1.0, 0), scale=(1,1,1)); key(CAT, 96, loc=(1.2, -1.2, 0), scale=(1,1,1)); key(CAT, 97, scale=(0,0,0))
key(CAT, 339, loc=(0.95, 0.9, Tz), scale=(0,0,0)); key(CAT, 340, loc=(0.95, 0.9, Tz-0.18), scale=(1,1,1), rot=(0,0,math.radians(180))); key(CAT, 348, loc=(0.95, 0.9, Tz-0.05), scale=(1,1,1)); key(CAT, 356, loc=(0.95, 0.9, Tz-0.2), scale=(1,1,1)); key(CAT, 357, scale=(0,0,0))
for e, x in ((AYA, -0.98), (RENP, 0.98)):
    key(e, 96, loc=(x, 0.4, 0), scale=(1,1,1)); key(e, 104, loc=(x, 0.1, 0.1)); key(e, 131, loc=(1.95, 0.9, 0.1), scale=(1,1,1)); key(e, 132, scale=(0,0,0))
scn.frame_set(0)
# ---------- save + export ----------
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "v1_bottle_table.blend"))
try:
    bpy.ops.export_scene.gltf(filepath=os.path.join(HERE, "v1_bottle_table.glb"), export_format='GLB', export_apply=True, export_animations=True, export_cameras=True, export_lights=True)
    print("GLB exported")
except Exception as ex: print("GLB export failed:", ex)
# ---------- render ----------
if do_render:
    scn.render.image_settings.file_format = 'PNG'
    for f in frames:
        scn.frame_set(f); scn.render.filepath = os.path.join(R, f"previz_f{f:03d}.png"); t = time.time(); bpy.ops.render.render(write_still=True)
        print(f"[FRAME] {f} {time.time()-t:.1f}s", flush=True)
print("[DONE]")
