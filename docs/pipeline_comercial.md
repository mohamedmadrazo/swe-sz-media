# Pipeline Streamline3X · Comerciales de 30 s o más (Sharp Zombie y siguientes)

Versión 1.0 · 2026-10-05 · Fuente de verdad del procedimiento. Lo ejecuta Claude como *loop* en cada comercial; el usuario entra en las puertas marcadas **G**.

## 0. Principios que no se negocian
1. **El producto es intocable**: etiqueta, tapón, forma y colores siempre desde el packshot/Element maestro y la textura real; `PRODUCT_LOCK` literal en todos los prompts; la lente de QA de producto tiene veto.
2. **Referencias antes que vídeo**: nada se rueda sin entorno, personajes, objetos y keyframes aprobados.
3. **Una variable por reintento, máximo 2 reintentos** por activo; después se decide con el usuario.
4. **Presupuesto con ledger**: `get_cost` antes de cada job caro, ledger JSON con job ids y créditos reales, aviso al 50 % y al 80 % del tope.
5. **Todo al repo**: docs, prompts, ledgers, texturas, escenas 3D, renders útiles (webp/mp4), manifest y dashboard; commit en español + push + PR borrador.
6. **QA con ojos**: cada imagen/vídeo se mira (sandbox `image_paths` o `Read` local) antes de darla por buena; QA adversarial por agentes en lotes grandes.

## Fase 1 · Guion → Biblia (0 créditos)
**Entrada**: guiones del usuario con las nociones primarias (historia, tono, duración, formato, producto, easter eggs).
**Salida**: `docs/<video>_bible.md` (identidad, look, paleta, personajes, escenario, tabla de beats con frames, planos, easter eggs, prohibiciones), `3d/<video>_beats.json` (fuente única de tiempos/cámara para 3D), lista de activos con modelo, refs y coste.
- Duración: pensar la tabla de beats para la duración objetivo (30 s = 720 fr @24) y dejar un corte a 15 s para cutdown.
- Bloques reutilizables: `PRODUCT_LOCK_NB`, `PRODUCT_LOCK_GPT`, `GLOW_LOCK`, `STYLE_LOCK`, `EXCLUSIONS_COMMON` (ver `docs/video1_prompt_brief_for_astra.md`).
- **G1**: el usuario valida biblia y beats (o se avanza con supuestos declarados si está ausente).

## Fase 2A · Referencias en sucio (Higgsfield) — ~60–120 cr
Ola 1 (producto, entorno, personajes) → Ola 2 (two-shot, objetos, escala, storyboard, keyframes, end card).
- Modelos: `nano_banana_pro` con Elements para todo lo que lleve producto o personajes recurrentes; `gpt_image_2_5` (`quality:high`, `flare` nuevo / `sunburst` "cambia solo X") para placas y fondos transparentes; `soul_location` para explorar localizaciones; `seedream_v5_pro` para texto exacto (end card).
- Clave de estilo **S**: una sola imagen que define el look; se pasa como primera referencia en todos los prompts. **Elegir S en la fase visual dominante del spot** (en Sharp Zombie, la fase oscura neon 3D) para que la fase iluminada no derive a cómic plano.
- QA por lotes: contact sheets en el sandbox; reintentos con una variable; QA adversarial por agentes (3 lentes) cuando el lote supera ~10 activos.
- Elements: crear `SZ-*` solo con activos aprobados (producto, personajes, troupe, gato, apartamento, contraetiqueta).
- **G2 "escogidos"**: el usuario marca las referencias definitivas (o Claude propone y lo deja por escrito en el ledger).

## Fase 2B · Diseño del set en Blender × Higgsfield (0 créditos salvo Meshy)
Una referencia por vez, en este orden: producto → mesa/objetos → arquitectura y ventana → luces → personajes/props → cámara.
- **3D Jutsu** (`scene_builder_3d_*`): blockout a escala real desde `beats.json` (metros, Principled, luces Point/Sun/Spot), una mutación por vez con guards frescos, stills con `query_python` (Eevee ≤3 por op; vídeo solo Workbench: Eevee en el worker ≈20 s/frame y el límite es 300 s).
- **Blender local** (`pip install bpy`, solo CYCLES CPU): `build_*_scene.py` con botella paramétrica, etiqueta frontal y contraetiqueta desde texturas reales (`build_label_texture.py`, `build_back_label.py`), personajes como recortes/billboards (`build_zombie_cutouts.py`) o meshes Meshy (`generate_3d` image_to_3d + rig + animación) cuando el dominio lo permita, previz y turntable.
- Cada referencia escogida se "traduce" al set: textura real donde la haya, Meshy/catálogo donde no, proxy animado como último recurso.
- Salida: `3d/<video>.blend/.glb` (local y 3D Jutsu), previz MP4, contact sheets por beat.
- **G3**: set completo aprobado (previz vista por el usuario).

## Fase 2C · Rodaje con el set preparado — ~60–150 cr
Tres cámaras posibles, de más controlada a más orgánica:
1. **Cámara virtual** (Blender): rodaje por planos desde `beats.json` (S1…Sn), 540×960 para drafts / 1080×1920 para final, Cycles 12–16 samples + denoise; `render_shoot.py` + `launch_shoot.sh`; sensor/claves ajustados para que la acción esté en cuadro (medir con `world_to_camera_view`).
2. **Móvil del usuario como driving video** (técnica Genjutsu): grabar en vertical 9:16 a 24/30 fps, trípode o gimbal, luz plana, 4–30 s por toma (límite de Restyle), con la **botella real o una maqueta a escala en plano** como ancla de escala y posición, actuación y movimiento de cámara reales (dolly a mano, tilt, push-in); sin estabilización agresiva ni HDR. Subir con `media_import_url` (puente: repo → jsDelivr para mp4; raw GitHub para png) o con el widget.
3. **Animatic IA** (Seedance 2.5 `draft:true` 480p, hasta 30 s) como comparativa y para validar ritmo; nunca como pieza final.
Transferencia de look: `hf_mult_motion_control` con **@Video1** = rodaje (1 o 2), **@Image1 LEAD** = keyframe de personajes, **@Image2 LOCATION** = keyframe del set, **@Image3** = clave S; `declined_preset_id` del preset "IN THE DARK" si el servidor lo sugiere. Preset oficial "Neon Graphic Cinematic 3D": `POST .../genjutsu/restyle/v1.0` con `preset_id` (API key en secretos) o Video → Genjutsu → Styles en la web.
- Lección: el driving manda. Blockout gris → salida desaturada; recortes/texturas reales → color y look completos.
- QA de vídeo: frames cada 2–3 s en el sandbox (etiqueta intacta, escala, continuidad, nada flotando), audio presente si aplica.
- **G4**: elegir las tomas buenas por plano; finalizar drafts Seedance a 1080p dentro de 7 días (`draft_job_id`).

## Fase 3 · Postproducción (Premiere)
Entrada: tomas finales 1080p (+ 4K con `upscale_video` si hace falta), end card, música licenciada.
1. Conformar a 24 fps, secuencia 1080×1920 (y 1920×1080 para la variante 16:9: reencuadre o tomas propias).
2. Cortes en los puntos de la biblia; holds de 1–2 s en producto; 1 s de aire antes del end card.
3. Color: LUT única del look (tomar la clave S como referencia de curva y saturación); igualar fase iluminada y oscura; negros limpios, lima solo en contornos.
4. Sonido: diseño (clic, pasos, plop), música desde el beat de despertar, duck en el hold final; mezcla a −14 LUFS (social) / −23 LUFS (broadcast).
5. Texto: solo end card (tagline JP, marca, legal validado por el cliente); nada de texto generado por IA en plano.
6. Exports: 9:16 1080×1920 H.264 20 Mbps, 16:9, 1:1 recorte; thumbnails; versión 15 s cutdown.
7. Checklist "mejor que la competencia": etiqueta legible en cada plano de producto, sin artefactos de manos/caras, continuidad de luz, ritmo musical, primer segundo con gancho, end card ≥2 s.

## Loop por sesión (lo que Claude hace cada vez)
1. Leer este documento y el `CLAUDE.md` del repo; cargar skills `higgsfield-prompt-director`, `higgsfield-genjutsu`, `senior-tool-prompter`.
2. `balance` → fijar tope y gates; crear/usar carpeta de proyecto en Higgsfield; `create_project` 3D Jutsu si no existe.
3. Fase 1 → G1 → Fase 2A (olas con Workflow de agentes: redacción → lint → generación → QA) → G2 → Fase 2B → G3 → Fase 2C → G4 → entregar paquete a Fase 3.
4. Cada fase: ledger JSON actualizado, `build_ledger_md.py`, `build_manifest_v1.py`, commit + push + PR; informe corto al usuario con créditos reales.
5. Esperas largas (renders, jobs): `ScheduleWakeup` o agente en segundo plano; nunca `sleep`.

## Lecciones aprendidas (2026-10-05, Sharp Zombie V1)
- Leer la textura real de la etiqueta antes de escribir el lock (las siluetas iban con brazos doblados, no "al frente").
- GPT Image y Nano Banana reproducen la etiqueta bien desde Element/packshot; GPT reposa figuras si se describen de más.
- `sunburst` sirve para "apagar la luz" sobre una imagen base; hay que decir explícitamente que el pendant está apagado.
- Eevee en el worker de 3D Jutsu es lento (timeouts); Workbench para vídeo; Cycles CPU en local (sin libEGL).
- `media_import_url` rechaza `application/octet-stream`: mp4 vía jsDelivr (commit SHA), png vía raw GitHub.
- Higgsfield sugiere el preset "IN THE DARK" ante escenas a oscuras: reenviar con `declined_preset_id`.
- Seedance 2.5 a 30 s funciona bien con 6 planos y dos cortes duros; el 15 s queda apretado.
- Elements de Kling solo con `start_image`; `sound:'off'` abarata.
