#!/usr/bin/env python3
"""Genera docs/video1_assets_ledger.md a partir de prompts/wave1_jobs.json (+ wave2_jobs.json, video_jobs.json si existen)."""
import json, os, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
def load(name):
    p = os.path.join(HERE, name)
    return json.load(open(p)) if os.path.exists(p) else None
w1, w2, vj, w3 = load('wave1_jobs.json'), load('wave2_jobs.json'), load('video_jobs.json'), load('wave3_jobs.json')
specs1 = load('wave1_specs_linted.json'); specs1 = specs1.get('specs', specs1) if isinstance(specs1, dict) else specs1
purpose1 = {s['id']: s.get('purpose', '') for s in (specs1 or [])}
out = []
out.append('# Ledger de activos — Sharp Zombie · Vídeo 1 "After Dinner, Tokyo" (línea `D_TOKYO_V1`)\n')
out.append(f'Generado: {datetime.date.today().isoformat()} · Proyecto Higgsfield folder `{(w1 or {}).get("folder_id","")}` · Clave de estilo S = job `30a2a515-405f-41f1-b785-2456b943d14d`\n')
if w1 and w1.get('balance'):
    b = w1['balance']; out.append(f"Saldo: inicio de sesión {b.get('start_session')} cr · tras ola 1 (A+B) {b.get('after_wave1_AB')} cr" + (f" · **final de sesión {b.get('end_session')} cr (gastados {b.get('spent_session')} de un tope de 600)**" if b.get('end_session') else '') + (f" · tras ola 2 {b.get('after_wave2')} cr" if b.get('after_wave2') else '') + (f" · tras drafts de vídeo {b.get('after_video')} cr" if b.get('after_video') else '') + '\n')
def table(title, jobs, purposes=None, qa=None):
    out.append(f'\n## {title}\n')
    out.append('| Activo | Modelo | Job id | Est. cr | Estado | QA director | Reintentos |')
    out.append('|---|---|---|---|---|---|---|')
    for k, e in jobs.items():
        ref = e.get('refine') or []
        rtxt = '; '.join(f"#{r.get('attempt')} `{str(r.get('job_id'))[:8]}` {r.get('verdict','')}" for r in ref) or '—'
        q = (qa or {}).get(k, '')
        url = e.get('url') or ''
        jid = e.get('job_id') or ''
        link = f'[`{jid[:8]}`]({url})' if url else f'`{jid[:8]}`'
        out.append(f"| `{k}` | {e.get('model','')} | {link} | {e.get('est_credits','')} | {e.get('status','')} | {q} | {rtxt} |")
if w1:
    table('Ola 1 — producto, entorno, personajes', w1['jobs'], purpose1, w1.get('director_qa'))
    if w1.get('elements'):
        out.append('\n### Elements (Higgsfield)\n'); out.append('| Element | id |'); out.append('|---|---|')
        for n, i in w1['elements'].items(): out.append(f'| `{n}` | `{i}` |')
    if w1.get('chosen'):
        out.append('\n### Referencias elegidas\n')
        for n, i in w1['chosen'].items(): out.append(f'- `{n}` → `{i}`')
    if w1.get('lock_fix'):
        lf = w1['lock_fix']; out.append(f"\n> Corrección de lock ({lf['date']}): «{lf['old']}» → «{lf['new']}» (fuente: {lf['source']}).")
    if w1.get('agent_qa'):
        out.append('\n### QA adversarial por agentes (3 lentes; veto de producto)\n')
        if w1.get('agent_qa_note'): out.append('> ' + w1['agent_qa_note'] + '\n')
        out.append('| Activo | Producto | Anatomía/física | Estilo | Veredicto | Sugerencia |'); out.append('|---|---|---|---|---|---|')
        for v in w1['agent_qa']:
            f = lambda d: ('✅' if d.get('pass') else '❌') + (f" {d.get('severity','')}" if not d.get('pass') else '')
            out.append(f"| `{v['asset_id']}` | {f(v['product_fidelity'])} | {f(v['anatomy_physics'])} | {f(v['style_continuity'])} | {v['overall']} | {v.get('fix_hint','')[:160]} |")
if w2:
    table('Ola 2 — two-shot, zombies 3D, escala, boards, keyframes, end card', w2['jobs'], None, w2.get('director_qa'))
    if w2.get('agent_qa'):
        out.append('\n### QA adversarial por agentes — ola 2\n')
        out.append('| Activo | Producto | Anatomía/física | Estilo | Veredicto | Sugerencia |'); out.append('|---|---|---|---|---|---|')
        for v in w2['agent_qa']:
            f = lambda d: ('✅' if d.get('pass') else '❌') + (f" {d.get('severity','')}" if not d.get('pass') else '')
            out.append(f"| `{v['asset_id']}` | {f(v['product_fidelity'])} | {f(v['anatomy_physics'])} | {f(v['style_continuity'])} | {v['overall']} | {v.get('fix_hint','')[:160]} |")
if w3:
    table('Ola v2 (2026-10-06) — keyframes iluminados con la clave de estilo oscura + recortes para Blender', w3['jobs'], None, w3.get('director_qa'))
    if w3.get('chosen'):
        out.append('\n### Elegidos v2\n')
        for n, i in w3['chosen'].items(): out.append(f'- `{n}` → `{i}`')
    if w3.get('decisions'):
        for n, t in w3['decisions'].items(): out.append(f'\n> Decisión ({n}): {t}')
    if w3.get('lessons'):
        out.append('\n### Lecciones v2\n')
        for t in w3['lessons']: out.append(f'- {t}')
if vj:
    out.append('\n## Drafts de vídeo (480p; `draft:true` caduca a los 7 días)\n')
    out.append('| Activo | Modelo | Job id | Cr | Estado | Caduca | Nota |'); out.append('|---|---|---|---|---|---|---|')
    for k, e in vj['jobs'].items():
        url = e.get('url') or ''; jid = e.get('job_id') or ''
        link = f'[`{jid[:8]}`]({url})' if url else f'`{jid[:8]}`'
        out.append(f"| `{k}` | {e.get('model','')} | {link} | {e.get('credits','')} | {e.get('status','')} | {e.get('expires','')} | {e.get('verdict','')} {e.get('note','')} |")
out.append('\n## 3D\n')
out.append('- 3D Jutsu "Sharp Zombie — Tokyo apt previz V1": proyecto `0d680169-83bc-4288-b579-1101122d639e` (revision 2) — https://higgsfield.ai/3d-jutsu/0d680169-83bc-4288-b579-1101122d639e')
out.append('- Blender local (bpy 5.0.1, Cycles CPU): `3d/build_v1_scene.py` → `3d/v1_bottle_table.blend/.glb`; turntable `video/v1_turntable_3d.mp4`; previz `img/v1_previz_bpy_f*.webp`.')
open(os.path.join(ROOT, 'docs', 'video1_assets_ledger.md'), 'w').write('\n'.join(out) + '\n')
print('docs/video1_assets_ledger.md', len(out), 'líneas')
