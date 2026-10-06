# Pipeline comercial Streamline3X · paquete para GPT-6 Astra

## Cómo usar este archivo

1. Abre Higgsfield Supercomputer (web) y, en el selector de modelo, elige **GPT-6 Astra**.
2. Pega el contenido completo de `docs/astra/system_prompt_pipeline_reviewer.md` en el campo de instrucciones del sistema si la interfaz lo ofrece. Si no lo ofrece, pégalo como primer mensaje añadiendo al final esta línea: "Estas son tus instrucciones. Responde solo OK y espera el siguiente mensaje con la tarea."; no pases al paso 3 hasta recibir ese OK.
3. Pega TODO lo que sigue a partir de la línea "## Mensaje para Astra" hasta el final del archivo (tarea + documento verbatim + anexo + formato) como UN solo mensaje de usuario, sin recortar nada ni cambiar el orden. Antes de enviar, comprueba que la línea "Fecha de hoy" de la tarea es la fecha real del envío y corrígela si no lo es (es la que Astra pondrá en la cabecera).
4. Guarda la respuesta completa (A–D) en `docs/astra/respuesta_astra.md` dentro de una rama nueva del repo (no sustituyas aún `docs/pipeline_comercial.md`) y pide a Claude Code que integre (A) sobre `docs/pipeline_comercial.md`, verifique cada fila de (B) y cada `[VERIFICAR]` de (C) contra el repo y Higgsfield, y pase la checklist (D) antes de hacer commit.
5. Si la respuesta se corta, responde: "continúa desde la sección X" (X = última sección completa recibida) y pega los trozos en orden. Nunca aceptes un (A) resumido, partido o fuera de un único bloque de código; si Astra pregunta en vez de entregar, responde: "Entrega igualmente las cuatro partes; lleva las dudas a Preguntas abiertas (C)".

## Mensaje para Astra

### Tarea
Fecha de hoy: 2026-10-05.
Mejora al máximo el documento `docs/pipeline_comercial.md` que va a continuación, pero SOLO a mejor: más robusto, escalable, mantenible y listo para producción con miles de ejecuciones por un agente (Claude Code) con un humano solo en las puertas G1–G4. Prioridades, en este orden: (1) criterios de aceptación medibles por fase y puerta; (2) control de costes e idempotencia (ledger antes de cada job caro, alertas al 50 % y 80 % del tope, condición de parada); (3) pre-mortem y recuperación ante los modos de fallo del anexo; (4) separación de invariantes y parámetros por cliente para escalar a otros productos.
Restricciones: respeta íntegramente el anexo de hechos verificados (nada se recalcula, redondea ni inventa); todo dato o herramienta que no conste en el documento ni en el anexo va marcado `[VERIFICAR: qué comprobar y dónde]`; conserva las fases 0, 1, 2A, 2B, 2C, 3, el loop por sesión, las lecciones aprendidas y las puertas G1–G4 (puedes añadir subsecciones o subpuertas al final de cada fase); los prompts de generación y los bloques de lock embebidos se conservan en inglés; el resto en español; la clave de estilo única es la fase oscura (KF6/KF7) y no se reabre. Salida diff-friendly: toca solo las líneas que mejoras.

### Documento actual: docs/pipeline_comercial.md (verbatim)
~~~~markdown
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
~~~~

### Anexo de hechos verificados (no modificar)
## Anexo de hechos verificados — pipeline_comercial.md (Streamline3X · Sharp Zombie V1) · 2026-10-05

Todo lo que sigue sale de archivos del repo `swe-sz-media` (o del `CLAUDE.md` del dashboard); la fuente va entre paréntesis al final de cada línea. Lo que no consta en ningún archivo se marca `[VERIFICAR]`; lo que solo consta en el encargo de esta sesión se marca `(encargo)`.

#### A. Herramientas y entorno disponibles
- **Quién ejecuta**: Claude Code como *loop* por comercial; el usuario entra en las puertas G1–G4, graba con su móvil y monta en Premiere (docs/pipeline_comercial.md). Skills cargadas antes de escribir prompts: `anthropic-skills:higgsfield-prompt-director`, `anthropic-skills:higgsfield-genjutsu`, `anthropic-skills:senior-tool-prompter` (.claude/skills/comercial-pipeline/SKILL.md; docs/pipeline_comercial.md §Loop).
- **MCP Higgsfield · imagen**: modelos `nano_banana_pro` (producto y personajes con Elements), `gpt_image_2_5` (placas, fondos transparentes, boards), `seedream_v5_pro` (texto exacto), `soul_location` (explorar localizaciones) (docs/pipeline_comercial.md; docs/video1_assets_ledger.md). Los nombres de herramienta `generate_image`/`generate_image_batch` no aparecen en ningún archivo del repo: constan solo en el encargo (encargo).
- **MCP Higgsfield · vídeo**: `generate_video` con `seedance_2_5` (`draft:true` 480p, `draft_job_id` para finalizar a 1080p), `kling3_0` y `hf_mult_motion_control` = Genjutsu motion transfer; parámetros confirmados en solo lectura con `models_explore action get` (0 créditos) (prompts/video_packages.json `model_facts`; docs/video1_restyle_howto.md).
- **MCP Higgsfield · otros**: `generate_3d` = Meshy image_to_3d con rig y animación (prompts/wave2_jobs.json `meshy`; docs/pipeline_comercial.md); Elements `SZ-*` creados solo con activos aprobados (docs/pipeline_comercial.md; el nombre de herramienta `manage_reference_elements` solo consta en el encargo) (encargo); `media_import_url` o "el widget" para subir el driving video (docs/pipeline_comercial.md; el nombre `media_upload_widget` solo consta en el encargo) (encargo); `sandbox_exec image_paths` para ver imágenes que el proxy bloquea (CLAUDE.md); `balance` al abrir sesión y `get_cost` antes de cada job caro (docs/pipeline_comercial.md; prompts/video_packages.json); `upscale_video` para 4K en post (docs/pipeline_comercial.md); `create_project` de 3D Jutsu si no existe (docs/pipeline_comercial.md). `jobs_wait`, `show_generation_by_ids`, `transactions`, `remove_background`, `reframe`, `video_analysis_*`: citados en el encargo, sin rastro en el repo `[VERIFICAR]`.
- **3D Jutsu** (`scene_builder_3d_*`): proyecto "Tokyo apt previz V1" `0d680169-83bc-4288-b579-1101122d639e` rev 2; blockout a escala real desde `beats.json`; una mutación por op con guards frescos; stills con `query_python` (Eevee ≤3 por op); vídeo solo Workbench (docs/pipeline_comercial.md; CLAUDE.md). Medido: Eevee en el worker ≈20 s/frame con timeouts de 300 s a 361 y 91 frames; Workbench 0,2–0,5 s/frame; previz Workbench 450×800 · 361 fr; clip guía 720×1280 f144–360 · 9 s (media `5c697f15`); 8 ops registradas (prompts/wave1_jobs.json `3d`).
- **Blender local**: bpy 5.0.1, solo CYCLES CPU (Eevee/Workbench abortan: sin libEGL) (CLAUDE.md; docs/video1_assets_ledger.md). Rodaje S5–S6: frames 204–360 a 540×960, 12 samples + OpenImageDenoise (3d/render_shoot.py); medido 8,4–9,5 s por frame (media ≈8,6 s), 157 frames en 22,6 min (3d/renders_shoot.log). Lanzamiento con `nohup` + `timeout 7000`, log `[FRAME]/[DONE]/[EXIT]`, matar solo con `pgrep -f "^python3 render_shoot.py"` (3d/launch_shoot.sh; CLAUDE.md). CPU: 4 núcleos según `nproc` en la máquina de esta sesión; no consta en ningún archivo `[VERIFICAR]`.
- **Scripts 3D**: `build_v1_scene.py` (botella paramétrica, etiqueta real, copas, mesa, cámara y coreografía desde `v1_beats.json`; 540×960; zombies como billboards `--cutouts` (por defecto) o cápsulas legacy `--no-cutouts`; samples por defecto 24; salida .blend/.glb) (3d/build_v1_scene.py); `build_zombie_cutouts.py` (5 siluetas RGBA negro mate + contorno lima #39FF14, solo PIL+numpy) (3d/build_zombie_cutouts.py); `build_label_texture.py`, `build_back_label.py`, `render_previz_anim.py` (360×640, paso 2 = 12 fps efectivos, 12 samples), `render_turntable.py` (docs/pipeline_comercial.md; 3d/render_previz_anim.py; listado de 3d/).
- **`3d/v1_beats.json`** = fuente única: fps 24, frames 0–360, 15 s, 9:16, unidades en metros Z-up, `layout`, `beats`, `shots` S1–S6 (35/50/50→85/100/85/85 mm), `camera_keys`, `lights` (pendant 2700 K 150 W off en f132–138, floor_lamp, kitchen_spill, moon_sun siempre), `glow`, `characters`, `easter_eggs` (3d/v1_beats.json).
- **GitHub**: repo `mohamedmadrazo/swe-sz-media` en GitHub Pages; `manifest.js` (`window.__SWE_MANIFEST__`) con 133 entradas: A_US 19 · B_JAPON 3 · C_SPIDERVERSE 32 · D_TOKYO_V1 77 · EXTRA 2 (manifest.js). `tools/build_manifest_v1.py` añade/actualiza solo D_TOKYO_V1 desde `prompts/*_jobs.json`, valida el JSON, respeta la indentación de 1 espacio y no toca otras líneas; salta `v1_env_00a/00d` (exploraciones con personas) (tools/build_manifest_v1.py). Ledger: `prompts/build_ledger_md.py` genera `docs/video1_assets_ledger.md` desde wave1/wave2/video_jobs + `wave1_specs_linted.json` (tope 600 escrito en el script) (prompts/build_ledger_md.py). Nunca editar manifest/ledger a mano (CLAUDE.md).
- **Dashboard `sharp-zombie-review`**: `index.html` único; lee `manifest.js` desde Pages o desde una rama con `?branch=<rama>` vía jsDelivr; galerías filtradas por `linea` y `escena`; `DEC`, `LBL` y `order` deben ir a la par; verificación con `node -e` y Playwright (sharp-zombie-review/CLAUDE.md).
- **Workflow de agentes**: redacción → lint → generación → QA con 3 lentes (producto, anatomía/física, estilo) y veto de producto, cuando el lote supera ~10 activos (SKILL.md; docs/pipeline_comercial.md); evidencia: `wave1_specs_linted.json` con `lint_report` y QA `wf_76ecdfca` sobre 23 activos (prompts/wave1_specs_linted.json; prompts/wave1_jobs.json `agent_qa`; docs/video1_assets_ledger.md). Regla: una variable por reintento, máximo 2 reintentos por activo (docs/pipeline_comercial.md §0).
- **Red**: el proxy local bloquea cloudfront y higgsfield.ai; importar mp4 vía `https://cdn.jsdelivr.net/gh/mohamedmadrazo/swe-sz-media@<sha>/...` y png vía `raw.githubusercontent.com` (CLAUDE.md); `media_import_url` rechaza `application/octet-stream` (docs/pipeline_comercial.md); caso real: `video/v1_shoot_blender_s5s6.mp4` → media `1effeb1f` (prompts/video_jobs.json).

#### B. Modelos y costes verificados
| Modelo | Uso | Parámetros clave | Coste | Límites / notas |
|---|---|---|---|---|
| `nano_banana_pro` | producto, personajes, keyframes, two-shot | 2k; Elements como `@nombre` (en la API `<<<uuid>>>` dentro del prompt; el backend lo reescribe a `@SZ-bottle-master`), nunca en medias; ≤8 refs; primera ref = clave de estilo | 2 cr/imagen (docs/video1_assets_ledger.md) | reproduce bien la etiqueta desde Element/packshot (docs/pipeline_comercial.md; docs/video1_prompt_brief_for_astra.md; prompts/video_packages.json) |
| `gpt_image_2_5` | placas, fondos transparentes, boards | `quality:high`; `flare` composición nueva / `sunburst` "cambia solo X"; sin Elements: `Image N` por orden de medias | 2,75 cr high 2k; 0,6 cr boards (docs/video1_assets_ledger.md; prompts/wave2_jobs.json) | reposa figuras si se describen de más (docs/pipeline_comercial.md) |
| `seedream_v5_pro` | texto exacto: end card, contraetiqueta provisional | textos entre comillas, tipografía descrita | 2,5 cr (docs/video1_assets_ledger.md) | — (docs/video1_prompt_brief_for_astra.md) |
| `soul_location` | explorar localizaciones | — | 0,5 cr (prompts/wave1_jobs.json; docs/video1_assets_ledger.md) | puede meter personas: env_00a/00d FAIL (docs/video1_assets_ledger.md) |
| `seedance_2_5` | animatic / candidata a máster | `mode omni_reference` (start_image + image_references `@Image N`; start_image no es un @Image), duration 4–30, 480p/720p/1080p, `draft` (480p finalizable en 7 días), `draft_job_id`, `generate_audio`, 9:16 | ≈3 cr/s a 480p: 8 s = 24 (est.), 15 s = 45 y 30 s = 90 (reales) (prompts/video_packages.json `cost_basis`; prompts/video_jobs.json) | 720p/1080p = 56/96 cr por 8 s según el encargo, no consta en el repo `[VERIFICAR]`; prompt ~1.000 palabras máx. (prompts/video_packages.json) |
| `kling3_0` | variantes A/B `v1_vid_04a/b` (planificadas, no ejecutadas) | duration 3–15, mode std/pro/4k, `sound:'off'` abarata, Elements `<<<id>>>` solo con `start_image`, prompt ≤2.500 car., ≤5 shots ≥3 s | ≈1,75 cr/s std sin sonido → 10 s = 17,5 (est. en paquetes); 5 s = 8,75 es un derivado del encargo, no consta literal `[VERIFICAR]` (prompts/video_packages.json) | sin `image_references` (prompts/video_packages.json; docs/video1_prompt_brief_for_astra.md) |
| `hf_mult_motion_control` (Genjutsu) | transferir look al driving video | roles `video_references` (@Video1) + `image_references` (@Image1 LEAD, @Image2 LOCATION, @Image3 STYLE opcional, quitar si el preflight la rechaza); 480p/720p/1080p; hereda el ratio del guía; prompt ≤3.900 car.; `preset_id` no confirmado por el contrato | 18 cr/7 s est. (≈2,57/s); paquete `v1_vid_05` est. 23; reales 27 cr/9 s y 20 cr/6,5 s (≈3/s) (prompts/video_packages.json; prompts/video_jobs.json; docs/video1_restyle_howto.md) | vídeo guía 4–30 s (docs/video1_restyle_howto.md) |
| Genjutsu Restyle (API pública) | preset "Neon Graphic Cinematic 3D" | `POST api.higgsfield.ai/higgsfield/genjutsu/restyle/v1.0` con `preset_id`, `video_url`, `image_urls` (≤5 API / 30 web), `resolution`; API key en secretos `HF_API_KEY_ID/HF_API_KEY_SECRET` | $0,318 / $0,681 / $1,632 por s (480/720/1080p), USD, no créditos (docs/video1_restyle_howto.md) | guía 4–30 s; conserva movimiento, cámara y audio (docs/video1_restyle_howto.md) |
| `generate_3d` (Meshy) | zombi rigged + animado | image_to_3d textured+rigged+animated, FunnyDancing_01 | 38 cr (job `ba71a51c`, GLB) (prompts/wave2_jobs.json) | desde `v1_char_05b` en A-pose (prompts/wave2_jobs.json) |

#### C. Límites y lecciones técnicas
- Leer la textura real de la etiqueta antes de escribir el lock: siluetas con brazos doblados y levantados, no "al frente" (docs/pipeline_comercial.md; prompts/wave1_jobs.json `lock_fix`).
- `sunburst` sirve para "apagar la luz" sobre una base; hay que decir explícitamente que el pendant está apagado (docs/pipeline_comercial.md).
- El driving manda: blockout gris → salida desaturada y zombies con forma de cápsula; recortes/texturas reales → color y look completos (docs/pipeline_comercial.md; prompts/video_jobs.json).
- Higgsfield sugiere el preset "IN THE DARK" ante escenas a oscuras: reenviar con `declined_preset_id` (docs/pipeline_comercial.md).
- Seedance 2.5 a 30 s funciona con 6 planos y dos cortes duros; el 15 s queda apretado (docs/pipeline_comercial.md; prompts/video_jobs.json).
- Elements de Kling solo con `start_image`; `sound:'off'` abarata (docs/pipeline_comercial.md; prompts/video_packages.json).
- Drafts Seedance `draft:true` caducan a los 7 días: anotar `expires` en `prompts/video_jobs.json` (CLAUDE.md).
- No subir carpetas de renders PNG (`renders/`, `renders_turntable/`, `renders_anim/`, `renders_shoot/`, `renders_jutsu/*.png`, `*.log`, `*.blend1` en 3d/.gitignore); sí webp/mp4 en `img/`, `poster/`, `video/` (CLAUDE.md; 3d/.gitignore).
- Clave de estilo S en fase iluminada hizo derivar la fase iluminada a cómic plano y cambió el estilo a mitad de vídeo (docs/video1_bible.md; docs/pipeline_comercial.md).
- QA por lotes: contact sheets en sandbox; QA adversarial ejecutada con el lock antiguo invalidó los fallos solo por pose (docs/video1_assets_ledger.md; prompts/wave1_jobs.json `agent_qa_note`).
- Defectos recurrentes para finales 1080p: silueta izquierda teñida de rojo (prod_01, prod_05), texto CAUTION corrupto/duplicado (prod_01, prod_05), tapón duplicado (prod_05), nombre/RIOJA ausentes y siluetas huecas en etiqueta apagada (prod_06), composición que calca la clave S (varios) (docs/video1_assets_ledger.md).
- Esperas largas: `ScheduleWakeup` o agente en segundo plano, nunca `sleep` (docs/pipeline_comercial.md).
- Inconsistencias del repo (verificadas): `prompts/video1_prompts.json` (citado en biblia §7 y brief de Astra) no existe; los prompts reales están en `wave1_specs_linted.json`, `wave2_packages.json`, `video_packages.json` (listado de prompts/). El lock de `docs/video1_restyle_howto.md` §"Lock de producto" aún dice "tres caminando brazos al frente" (lock antiguo; corregir). Estimación de gasto 234,33 vs real 345,33 sin desglose (prompts/wave1_jobs.json `balance`). `v1_vid_05` estimado 23 cr en paquetes, 27 reales (prompts/video_packages.json; prompts/video_jobs.json).

#### D. Ids fijos que no se tocan
- Carpeta de proyecto Higgsfield: `af60db5b-3cf0-444c-8218-287a76fde27d` (CLAUDE.md).
- Elements: SZ-bottle-master `de0c221b-6bd9-4ab5-912b-c6840b2423cc` · SZ-bottle-back `29cbd6df-d8cd-405f-aa0a-3974b6cfb28c` · SZ-aya `65a0c653-c433-4c10-a435-a4ce5504f0a2` · SZ-ren `c800522c-a722-4f47-bb45-2f32899d7e45` · SZ-zombies-glow `5915e7ac-09c7-4efc-bf78-a1904ace295b` · SZ-cat `2ab36fde-48a2-4f46-ba0c-0e3c66e86f84` · SZ-apartment `0199fa74-cff0-459d-801c-fae3153bf8bd` (CLAUDE.md; prompts/wave1_jobs.json `elements`); provisional SZ-bottle-back-PROV `6ea674e7-12b6-442a-98e0-b6ae20dd9a9e` (prompts/wave1_jobs.json).
- Refs: packshot `aade31ed-0151-469c-bc50-513aff07bb68` · foto real glow `a1c24793-cf2e-4f5b-8b0f-4e69b82bbbfa` · clave S iluminada `30a2a515-405f-41f1-b785-2456b943d14d` (CLAUDE.md).
- **Look definitivo = fase oscura**: KF6 `94052ac7-c2c1-41c9-a7ff-1340c8b5e82d`, KF7 `fdead37f-5f7c-4afe-88d8-3ce13f5aa905` (CLAUDE.md; docs/video1_bible.md).
- Referencias elegidas ola 1: env_02 `4cd1483a-ce45-4e44-9e52-b7982a98c490` · prod_02 `8cb396b0-23d4-4699-bbd6-11d2bd331108` · prod_03 `ea445def-13c9-4e96-b66c-7a3e98fef059` · prod_03_alt_nb `f4c8aa8f-d70e-45c5-8ebb-d04291380bd9`; ola 2: kf_02 `b1688f56-40da-449d-b867-e64e79106a15` · kf_06 `94052ac7-c2c1-41c9-a7ff-1340c8b5e82d` (prompts/wave1_jobs.json `chosen`; prompts/wave2_jobs.json `chosen`).
- 3D Jutsu `0d680169-83bc-4288-b579-1101122d639e` rev 2; medias: clip guía 3D Jutsu `5c697f15-f4a7-4c98-846e-a7406650e8c0`, rodaje Blender `1effeb1f`, contraetiqueta `9d3e80d0-3b86-4008-9d52-c461fffa8ad1` (CLAUDE.md; prompts/wave1_jobs.json; prompts/video_jobs.json).
- Jobs de vídeo: `v1_vid_05` `27122a66-e577-4cee-be62-4cb9c77006d3` · `v1_vid_01` `443cecb3-9eba-444b-b543-fff53185eb38` · `v1_vid_01_30s` `52247062-10f6-4f36-996e-e07eaea31814` · `v1_vid_05b` `602dfef6-8d56-47d9-a3f8-af2ce7add1df`; Meshy `ba71a51c-ef22-47ea-9e1f-ab6cef92b647` (prompts/video_jobs.json; prompts/wave2_jobs.json).
- Texturas reales: `3d/textures/label_front.png` (recorte del packshot) y `label_back.png` (reconstrucción 1:1 con PIL en `3d/build_back_label.py`; pendiente el escaneo real en `img/ref_contraetiqueta_real.png`) (prompts/wave1_jobs.json `lock_fix`, `back_label`; CLAUDE.md).

#### E. Qué pasó en el vídeo 1 (2026-10-05)
- Fase 1: biblia de 15 s, 9 beats, planos S1–S6, cortes duros a 5,5 y 8,5 s, música a 7,5 s, 7 easter eggs, prohibiciones; `3d/v1_beats.json` como fuente única (docs/video1_bible.md).
- Ola 1 (lotes A/B/C, 26 jobs): producto `v1_prod_01–07c` y `09` (no hay 08), entorno `v1_env_00a–d`, `02–05b`, `07` (no hay 06), personajes `v1_char_01/01n/02/02n/04/06`; reintentos con una variable: prod_02 → `8cb396b0`, prod_03 → `ea445def` y `f4c8aa8f`, env_02 → `4cd1483a`; FAIL env_00a/00d por personas; Elements SZ-* creados; saldo 2988 → 2936,42 cr (docs/video1_assets_ledger.md; prompts/wave1_jobs.json; prompts/wave1_batch_A/B/C.json).
- Corrección del lock tras leer `label_front.png`; QA adversarial `wf_76ecdfca` sobre 23 activos (3 lentes): **12 approved, 11 fix**; los fallos solo por pose no valen; lista de mejora para finales (docs/video1_assets_ledger.md; prompts/wave1_jobs.json `agent_qa`).
- Ola 2 (lotes D/E/F, 30 jobs): two-shot `char_03`, salida `char_08`, zombies transparentes `char_05a–d`, escala 5 cm `char_07`, contraetiqueta real `prod_10a/b` (fix#1 `834234c4`/`0aa7713f`), end card JP `v1_endcard` (legal placeholder), KF1–KF8 + 16:9 `kf_01w/08w` (kf_02 fix#1 `b1688f56`; kf_06 fix#2 `94052ac7` tras fix#1 `7af81b6e` FAIL por etiqueta re-tipografiada), boards 01–10 a 0,6 cr (docs/video1_assets_ledger.md; prompts/wave2_jobs.json).
- 3D: 3D Jutsu rev 2 con 8 ops (blockout, fix seating/glow, stills, previz Workbench, clip guía); Blender local `.blend/.glb`, turntable, previz bpy 360×640 a 12 fps; Meshy zombi bailando 38 cr; rodaje S5–S6 (f204–360) → `video/v1_shoot_blender_s5s6.mp4` (prompts/wave1_jobs.json `3d`; 3d/renders_shoot.log; prompts/video_jobs.json).
- Drafts de vídeo: `v1_vid_05` Genjutsu sobre previz 3D Jutsu, 9 s, 27 cr → PARCIAL (gris, cápsulas); `v1_vid_01` Seedance 15 s, 45 cr → PASS apretado, caduca 2026-10-12; `v1_vid_01_30s` Seedance 30 s, 90 cr → PASS, candidata a máster, caduca 2026-10-12; `v1_vid_05b` Genjutsu sobre rodaje Blender, 6,5 s, 20 cr → PASS, pipeline Blender→Genjutsu validado (leve flotación de pies en algún frame) (prompts/video_jobs.json).
- Planificados sin ejecutar (con paquete en `video_packages.json`, sin entrada en `video_jobs.json`): `v1_vid_02` Seedance 8 s (24 est.), `v1_vid_04a/b` Kling 10 s (17,5 est. cada). Smoke test Restyle `v1_vid_03` 5 s: solo citado en notas, sin paquete ni job `[VERIFICAR]` (prompts/video_packages.json; docs/video1_restyle_howto.md).
- Saldo: 2988 → 2936,42 (ola 1 A+B) → 2753,67 (`after_wave2_and_drafts`) → **2642,67 final; gastados 345,33 de un tope de 600** (prompts/wave1_jobs.json `balance`; prompts/video_jobs.json `balance`; docs/video1_assets_ledger.md).
- Decisión de look: el usuario prefiere el draft 30 s `52247062` y su segunda parte (3D neon, rims magenta/cian, negros limpios); KF6/KF7 pasan a clave única para TODOS los planos; regenerar KF1–KF3 y el two-shot; una sola LUT en post; versión 30 s = ×2 en frames salvo holds (gato 1 s, estatuas 1 s, final 2 s) (docs/video1_bible.md).
- Funcionó: etiqueta fiel desde Element/packshot; recortes reales como driving; Seedance 30 s con 6 planos. Falló: clave S iluminada; blockout gris como driving; Eevee en el worker; `media_import_url` con octet-stream (docs/pipeline_comercial.md; prompts/video_jobs.json).

#### F. Restricciones del encargo para Astra
- No cambiar ni inventar ids, job ids, costes, saldos, límites ni nombres de herramientas; todo dato nuevo o dudoso va marcado `[VERIFICAR]` (encargo).
- Mantener la estructura: fase 0 principios · 1 biblia (G1) · 2A referencias (G2) · 2B set 3D (G3) · 2C rodaje y transferencia de look (G4) · 3 post · loop por sesión · lecciones (docs/pipeline_comercial.md).
- Español en el documento; los prompts de generación embebidos y los bloques `PRODUCT_LOCK_NB`, `PRODUCT_LOCK_GPT`, `GLOW_LOCK`, `STYLE_LOCK`, `EXCLUSIONS_COMMON` se conservan en inglés (docs/video1_prompt_brief_for_astra.md; docs/pipeline_comercial.md §Fase 1).
- Producto intocable: tapón de rosca negro (nunca corcho), etiqueta amarilla con franjas caution, blackletter rojo oscuro, RIOJA, D.O.Ca., tres zombis en marcha de perfil con brazos doblados y levantados + uno agachado + manita; a oscuras brillan solo los contornos en lima fino, nunca el texto (CLAUDE.md).
- Clave de estilo única = fase oscura KF6/KF7; S iluminada ya no es referencia de estilo (CLAUDE.md; docs/video1_bible.md).
- Solo a mejor: más robusto, escalable y mantenible para miles de ejecuciones, sin romper lo que ya funciona ni añadir capacidades que el repo no demuestra (encargo).

### Formato de salida obligatorio
Sin preámbulos ni despedidas. Reglas que aplican a las cuatro partes: nada que no conste en el documento o en el anexo (no inventar herramientas, modelos, parámetros, costes, ids ni límites); todo dato dudoso o ausente con `[VERIFICAR: qué comprobar y dónde]`, nunca un valor plausible; fases 0, 1, 2A, 2B, 2C, 3, loop por sesión, lecciones aprendidas y puertas G1–G4 conservadas; español, con los prompts de generación y los bloques de lock embebidos en inglés y literales. Cuatro partes, en este orden:
- **(A)** Documento completo mejorado en Markdown, en UN único bloque de código, listo para sustituir `docs/pipeline_comercial.md`; versión incrementada y fecha de cabecera 2026-10-05.
- **(B)** Tabla de cambios: sección · cambio (antes → después) · por qué (modo de fallo o debilidad que corrige) · riesgo/coste de aplicarlo; incluye supresiones y consolidaciones.
- **(C)** Preguntas abiertas numeradas: cada `[VERIFICAR]` y cada decisión que requiera al usuario, con su impacto si queda sin respuesta y la opción recomendada.
- **(D)** Checklist de verificación para el ejecutor (Claude Code): casillas de una línea para comprobar en el repo y en Higgsfield antes del commit.
Si el resultado no cabe en una respuesta, entrega (A) completo, avisa de que (B)–(D) siguen en la siguiente y divide por secciones; nunca recortes (A).
