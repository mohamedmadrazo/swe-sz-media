#!/usr/bin/env python3
"""Añade/actualiza las entradas de la línea D_TOKYO_V1 en manifest.js a partir de prompts/*_jobs.json y archivos locales.
Valida el JSON resultante, respeta la indentación de 1 espacio del archivo y no toca las otras líneas."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = 'https://mohamedmadrazo.github.io/swe-sz-media'
MAN = os.path.join(ROOT, 'manifest.js')
def load(p):
    p = os.path.join(ROOT, 'prompts', p)
    return json.load(open(p)) if os.path.exists(p) else None
w1, w2, vj = load('wave1_jobs.json'), load('wave2_jobs.json'), load('video_jobs.json')
specs1 = load('wave1_specs_linted.json'); specs1 = specs1.get('specs', specs1) if isinstance(specs1, dict) else (specs1 or [])
purpose = {s['id']: s.get('purpose', '') for s in specs1}
if w2:
    for k, e in w2['jobs'].items(): purpose.setdefault(k, e.get('purpose', ''))
ESC = [(r'^v1_prod_', 'PROD'), (r'^v1_env_', 'ENV'), (r'^v1_char_0[12]', 'SHEET'), (r'^v1_char_04|^v1_char_05|^v1_char_07', 'ZSHEET'), (r'^v1_char_06', 'CAT'), (r'^v1_char_', 'SHEET'), (r'^v1_board_(\d+)', 'B{n}'), (r'^v1_kf_(\d+)', 'KF{n}'), (r'^v1_endcard', 'END')]
def escena(k):
    for pat, e in ESC:
        m = re.match(pat, k)
        if m:
            return e.replace('{n}', str(int(m.group(1)))) if '{n}' in e else e
    return 'MISC'
def short(txt, n=140):
    txt = (txt or '').replace('\n', ' ').strip()
    return txt if len(txt) <= n else txt[:n - 1].rstrip() + '…'
entries = []
def img_entry(k, e, primaria=False):
    url = e.get('url')
    if not url: return
    ref = [r for r in (e.get('refine') or []) if r.get('url') and str(r.get('verdict', '')).startswith('PASS')]
    chosen = e
    if ref: chosen = ref[-1]  # último reintento aprobado
    w, h = (e.get('size') or '0x0').split('x') if e.get('size') else ('0', '0')
    entries.append({"id": k, "tipo": "imagen", "linea": "D_TOKYO_V1", "escena": escena(k), "desc": short(purpose.get(k, k)), "status": "COMPLETED", "primaria": primaria, "w": int(w), "h": int(h), "dur": 0, "src": chosen['url'], "poster": None, "origen": "higgsfield", "job_id": chosen.get('job_id'), "model": e.get('model')})
if w1:
    skip = {'v1_env_00a', 'v1_env_00d'}  # exploraciones con personas: no se publican
    for k, e in w1['jobs'].items():
        if k in skip or e.get('status') != 'completed': continue
        img_entry(k, e, primaria=(k == 'v1_prod_01'))
if w2:
    for k, e in w2['jobs'].items():
        if e.get('status') != 'completed': continue
        img_entry(k, e, primaria=(k == 'v1_kf_01'))
if vj:
    for k, e in vj['jobs'].items():
        if e.get('status') != 'completed' or not e.get('url'): continue
        entries.append({"id": k, "tipo": "video", "linea": "D_TOKYO_V1", "escena": e.get('escena', 'DRAFT'), "desc": short(e.get('desc', k)), "status": "COMPLETED", "primaria": e.get('primaria', False), "w": e.get('w', 0), "h": e.get('h', 0), "dur": e.get('dur', 0), "src": e['url'], "poster": e.get('poster'), "origen": "higgsfield", "job_id": e.get('job_id'), "model": e.get('model')})
# locales
for f in sorted(os.listdir(os.path.join(ROOT, 'img'))):
    m = re.match(r'v1_previz_bpy_f(\d+)\.webp$', f)
    if m:
        entries.append({"id": f[:-5], "tipo": "imagen", "linea": "D_TOKYO_V1", "escena": "PREVIZ", "desc": f"Previz Blender local (Cycles) · frame {int(m.group(1))} / 360", "status": "COMPLETED", "primaria": False, "w": 540, "h": 960, "dur": 0, "src": f"{PAGES}/img/{f}", "poster": None, "origen": "blender"})
    m = re.match(r'v1_previz_3djutsu_f(\d+)\.webp$', f)
    if m:
        entries.append({"id": f[:-5], "tipo": "imagen", "linea": "D_TOKYO_V1", "escena": "PREVIZ", "desc": f"Previz 3D Jutsu (Eevee) · frame {int(m.group(1))} / 360", "status": "COMPLETED", "primaria": False, "w": 360, "h": 640, "dur": 0, "src": f"{PAGES}/img/{f}", "poster": None, "origen": "3djutsu"})
if os.path.exists(os.path.join(ROOT, 'video', 'v1_turntable_3d.mp4')):
    entries.append({"id": "v1_turntable_3d", "tipo": "video", "linea": "D_TOKYO_V1", "escena": "TURN", "desc": "Turntable 3D de la botella (Blender local, pasada encendida + pasada glow)", "status": "COMPLETED", "primaria": False, "w": 540, "h": 960, "dur": 6, "src": f"{PAGES}/video/v1_turntable_3d.mp4", "poster": f"{PAGES}/poster/v1_turntable_3d.webp", "origen": "blender"})
if os.path.exists(os.path.join(ROOT, 'video', 'v1_previz_3djutsu.mp4')):
    entries.append({"id": "v1_previz_3djutsu", "tipo": "video", "linea": "D_TOKYO_V1", "escena": "PREVIZ", "desc": "Previz completa 15 s (3D Jutsu, blockout animado: cámara, apagón, glow, coreografía)", "status": "COMPLETED", "primaria": True, "w": 360, "h": 640, "dur": 15, "src": f"{PAGES}/video/v1_previz_3djutsu.mp4", "poster": f"{PAGES}/poster/v1_previz_3djutsu.webp", "origen": "3djutsu"})
if os.path.exists(os.path.join(ROOT, 'video', 'v1_previz_bpy.mp4')):
    entries.append({"id": "v1_previz_bpy", "tipo": "video", "linea": "D_TOKYO_V1", "escena": "PREVIZ", "desc": "Previz 15 s (Blender local, Cycles 12 fps)", "status": "COMPLETED", "primaria": False, "w": 360, "h": 640, "dur": 15, "src": f"{PAGES}/video/v1_previz_bpy.mp4", "poster": f"{PAGES}/poster/v1_previz_bpy.webp", "origen": "blender"})
for g in ('v1_bottle_table.glb', 'v1_tokyo_previz_3djutsu.glb'):
    if os.path.exists(os.path.join(ROOT, '3d', g)):
        entries.append({"id": g[:-4], "tipo": "3d", "linea": "D_TOKYO_V1", "escena": "GLB", "desc": "Escena 3D descargable (GLB) · " + ("Blender local" if 'bottle' in g else "3D Jutsu"), "status": "COMPLETED", "primaria": False, "w": 0, "h": 0, "dur": 0, "src": f"{PAGES}/3d/{g}", "poster": None, "origen": "blender" if 'bottle' in g else "3djutsu"})
# merge en manifest.js
src = open(MAN, encoding='utf-8').read()
m = re.match(r'^(window\.__SWE_MANIFEST__=)(\[.*\])(;\s*)$', src, re.S)
assert m, 'formato manifest.js inesperado'
data = json.loads(m.group(2))
data = [d for d in data if d.get('linea') != 'D_TOKYO_V1']
ids = set(d['id'] for d in data)
for e in entries:
    assert e['id'] not in ids, f"id duplicado {e['id']}"; ids.add(e['id'])
data.extend(entries)
out = m.group(1) + json.dumps(data, indent=1, ensure_ascii=False) + ';\n'
json.loads(out[len(m.group(1)):-2])  # valida
open(MAN, 'w', encoding='utf-8').write(out)
print(f'manifest.js: {len(entries)} entradas D_TOKYO_V1 · total {len(data)}')
for e in entries: print(' ', e['id'], e['tipo'], e['escena'], e['origen'])
