#!/usr/bin/env python3
"""Genera docs/video1_storyboard.md (boards + keyframes + beats) desde prompts/wave2_jobs.json y wave2_brief.json."""
import json, os
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
W=json.load(open(os.path.join(HERE,'wave2_jobs.json'))); B=json.load(open(os.path.join(HERE,'wave2_brief.json')))
def url(k):
    e=W['jobs'].get(k,{}); ref=[r for r in (e.get('refine') or []) if r.get('url') and str(r.get('verdict','')).startswith('PASS')]
    return (ref[-1]['url'] if ref else e.get('url')) or ''
out=['# Storyboard — Sharp Zombie · Vídeo 1 "After Dinner, Tokyo" (15 s · 9:16 + 16:9)\n',
'Look: preset Genjutsu Restyle "Neon Graphic Cinematic 3D". Sin diálogo, solo música (arranca a 7.5 s). Cortes duros en 5.5 s y 8.5 s. Beats y cámara en `docs/video1_bible.md` y `3d/v1_beats.json`.\n',
'## Boards (10)\n','| Board | Beat | Imagen |','|---|---|---|']
for it in B['groups']['B_boards']['items']:
    out.append(f"| **{it['label']}** | {it['beat']} | [{it['id']}]({url(it['id'])}) |")
out+=['\n## Keyframes en el look (2K)\n','| KF | Escena | Imagen |','|---|---|---|']
for a in B['groups']['C_keyframes']:
    out.append(f"| `{a['id']}` | {a['purpose'][:150]} | [ver]({url(a['id'])}) |")
out+=['\n## Personajes, producto y end card\n','| Activo | Uso | Imagen |','|---|---|---|']
for a in B['groups']['A_char_prod']:
    out.append(f"| `{a['id']}` | {a['purpose'][:140]} | [ver]({url(a['id'])}) |")
out+=['\n## Easter eggs\n','- EE1 el gato cruza y mira a cámara (beat 2) y asoma al final (beat 9)','- EE2 el zombie agachado no se despierta (beat 5)','- EE3 la manita anda con los dedos (beat 6)','- EE4 limbo bajo los palillos (beat 7)','- EE5 DJ con el tapón de rosca (beat 7)','- EE6 se congelan en pose de etiqueta al pasar la sombra de Ren (beat 7)','- EE7 el maneki-neko mueve la pata al compás (beat 7)']
open(os.path.join(ROOT,'docs','video1_storyboard.md'),'w').write('\n'.join(out)+'\n'); print('docs/video1_storyboard.md', len(out))
