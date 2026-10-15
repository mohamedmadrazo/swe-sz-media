# HANDOFF · Revisión de Satoshi (socio de María) · 15-oct-2026

Documento de traspaso entre sesiones. La sesión que lo abra debe leerlo entero antes de tocar nada y seguir el orden de la sección 6.

## 0. Cómo arrancar la sesión nueva (para que no pida permiso a cada paso)

- Abre la sesión **solo con el repo `mohamedmadrazo/swe-sz-media`**, rama `claude/confident-goldberg-rw44ia`. Con un único repo la sesión lee `.claude/settings.json`, que ya autoriza los comandos habituales (python3, ffmpeg, git, curl, ls, cat, grep, find, mkdir, cp, node, bash, nohup), lectura y edición de archivos, y todas las herramientas de Higgsfield, GitHub y sesiones remotas. Lo que no está en esa lista (por ejemplo sed, awk, rm o los flujos de agentes) lo decide el modo Auto, que deja pasar la mayoría.
- Elige el modo **Auto** en el selector junto a la caja de texto. Si la sesión se reinicia, comprueba que sigue en Auto.
- Primer mensaje sugerido: «Lee HANDOFF.md y continúa la revisión de Satoshi desde la sección 6, sin pedir permiso».
- El dashboard (`sharp-zombie-review`) es otro repo. Se actualiza al final en una sesión aparte con solo ese repo (sección 6, paso 8).

## 1. Contexto mínimo

- Cliente: SWE · Sharp Zombie Rioja (etiqueta que brilla en la oscuridad). Agencia: Streamline3X. Contacto: María; revisor: Satoshi, su socio.
- Repos: `swe-sz-media` (assets, `manifest.js`, docs, prompts, ledgers) y `sharp-zombie-review` (dashboard). PR borrador #1 abierta en ambos, rama `claude/confident-goldberg-rw44ia`.
- Reglas del repo en `CLAUDE.md` (ids fijos, lock de producto, reglas técnicas) y procedimiento en `docs/pipeline_comercial.md` (skill `comercial-pipeline`).
- Higgsfield: workspace `6f3d1bc8-8c68-4180-a5b0-9582e2da64ea`; proyecto del vídeo 1 `af60db5b-3cf0-444c-8218-287a76fde27d`; Test Lab JP `faa6089d-c81e-4381-9eac-0be3e801600b`. Saldo el 14-oct: **1578,04 cr**.
- Red: el proxy local bloquea cloudfront y higgsfield.ai. Todo el trabajo de medios se hace en `sandbox_exec` de Higgsfield (tiene internet, ffmpeg, Pillow, numpy, faster-whisper). Para ver imágenes: `image_paths` (máx. 4, ≤512 KiB).

## 2. Lo que dijo Satoshi (WhatsApp de María, 14-oct)

María le envió una selección de 4 vídeos. Comentarios literales:

1. **Vídeo 1, Tokio (luna y copas):** «El primer vídeo me gusta mucho porque tiene una historia. Hay varios detalles divertidos y me ha parecido muy entretenido. Creo que, con un par de pequeños ajustes, ¡quedaría perfecto! Por ejemplo, en la escena en la que el hombre y la mujer retiran los platos, estaría bien que la mujer hiciera algún pequeño gesto, como hablar un poco con el hombre o girar ligeramente la cabeza, como si hubiera notado algo. Creo que daría un toque de misterio y sería aún más interesante. También creo que el sonido al beber el vino podría ser un poco más suave. Ahora se escucha demasiado fuerte y, en algunos casos, puede dar una impresión un poco vulgar.»
2. **Vídeo 2, fiesta en casa:** «El segundo vídeo, que recuerda a una fiesta en casa con amigos, es sencillo, pero me gusta mucho. Transmite muy bien cómo queremos que los jóvenes disfruten de nuestros vinos.» → **sin cambios**.
3. y 4. **Los dos de izakaya:** «me ha gustado mucho el sonido del ambiente animado del primero. También me parece muy divertida la escena en la que apagan la luz con la mano. Es una situación imposible en la realidad, y precisamente por eso tiene mucho humor. Una cosa más: al final de esta escena se escucha la risa de una mujer. Si es así, creo que sería mejor que la mano que apaga la luz también fuera de una mujer. Eso sí, creo que el efecto de la etiqueta iluminada es un poco exagerado. En cambio, en el último vídeo de Zombie, en el que aparecen las copas, la iluminación de la etiqueta es mucho más natural. Me gusta mucho más así. Además, ¡los yakitori tienen una pinta buenísima! En general, se nota un poco que los vídeos están [texto cortado por «Leer más»] …nivel de calidad muy alto! Muchas gracias por tu trabajo!»
   - **Pendiente:** pedir al usuario el texto completo del párrafo cortado («se nota un poco que los vídeos están…»), por si pide algo más.

La carpeta «VIDEOS REVISION» que mencionó el usuario no aparece ni en Higgsfield ni en Drive; los cuatro vídeos se identificaron comparando las miniaturas con el historial (sección 3).

## 3. Los cuatro vídeos identificados

| # | Vídeo | Job Higgsfield | Modelo · formato | Petición |
|---|---|---|---|---|
| 1 | Tokio "After Dinner" 30 s | `d45bbfb0-b6b7-4bce-b33a-6981a516b7f4` | Seedance 2.5, 480×854, 24 fps, 30,05 s, con audio. Draft **caducado el 13-oct** (ya no se puede finalizar a 1080p con `draft_job_id`) | Gesto de la mujer + sorbo más suave |
| 2 | Fiesta en casa 8 s | candidatos `9f558fcf…` (Kling 720p), `8a9f1c36…` / `49f55905…` (Seedance 480p) | — | Ninguna |
| 3 | Izakaya, la mano apaga la luz | `66468164-b46b-41ab-a8c7-62554cc779ae` | Cinema Studio 3.0, 720×1280, 8,06 s, con audio | Mano de mujer + brillo natural |
| 4 | Izakaya con copas | `192387a8-fe20-48f5-b195-63c1977b72f1` | Seedance 2.5, 1080×1920, 8 s | Ninguna. Es la **referencia de brillo**: su end frame es el image job `f1763dde-ff78-4fcb-8280-6ebf07b51d23` |

URLs de descarga (para el sandbox):
- 1: `https://d8j0ntlcm91z4.cloudfront.net/user_3BP9AlN7MxU50eaw9ZlO6ny5hI2/hf_20261006_181312_d45bbfb0-b6b7-4bce-b33a-6981a516b7f4.mp4`
- 3: `https://d8j0ntlcm91z4.cloudfront.net/user_3BP9AlN7MxU50eaw9ZlO6ny5hI2/hf_20260928_230348_66468164-b46b-41ab-a8c7-62554cc779ae.mp4`
- 4: `https://d8j0ntlcm91z4.cloudfront.net/user_3BP9AlN7MxU50eaw9ZlO6ny5hI2/hf_20260928_230349_192387a8-fe20-48f5-b195-63c1977b72f1.mp4`

## 4. Hallazgos técnicos (medidos en el sandbox)

**Vídeo 1 (d45bbfb0).** Cortes detectados (ffmpeg scene > 0,25): 7,875 · 11,0 · 13,083 · 17,0 · 23,958 s.
- 0–7,875 S1 plano general: 0,3–1,5 beben los dos (copa en la boca); 2,6–3,0 brindis (clink); 3,3–4,3 risas; 5–7 el gato cruza (maullido ~5,3); 7–7,875 se levantan y cogen platos.
- **7,875–11,0 S2, el plano de los platos:** cámara fija a nivel de mesa, botella en primer término centrada, dos copas, plato con restos. 0,1–0,5 s del plano ambos detrás de la mesa con los platos; ~0,5 él sale por la derecha; 0,9–2,1 ella camina de espaldas hacia la puerta del fondo; 2,1–3,1 ella en la puerta.
- 11,0–13,08 mesa vacía/apagón · 13,08–17 macro etiqueta · 17–23,96 baile en la mesa · 23,96–30 copas, luna y gato.
- **El sorbo ruidoso:** Whisper transcribe **«Shushushush» entre 1,80 y 2,56 s** (sorbo/succión, energía grave fuerte 1,9–2,4 s). Justo después, 2,6–2,9 s, el clink del brindis (agudos), que hay que conservar. 0,0–1,68 y 3,26–4,32 son risas («Ha ha ha»), se conservan.
- **Sin comprobar:** si hay más sonidos de beber en 17–30 s (zombis cayendo en las copas, con música debajo). Satoshi dice «en algunos casos»: revisar con Whisper el tramo 6–30 s y el espectro antes de cerrar.

**Vídeo 3 (66468164).** 0–2,5 botella fija en la barra con farolillos y yakitori · 2,5 entra una mano de hombre por la derecha · ~3,5 tira del cordón del farol (clic 3,6 s) · leve push-in de cámara · ~4,5 otra mano arriba a la izquierda junto a un farol · **5,4 apagón** (pico −11 dB) · 5,5–8,0 primer plano de la etiqueta con **toda la cara de la etiqueta verde, letras incluidas** (el «exagerado») · 5,8–7,2 silencio total · **7,2–8,0 risa de mujer**. Prompt original: «A hand flips the bar lights off; … the barman laughs off-screen».

## 5. Estado del trabajo

Hecho:
- Vídeos identificados, tiempos medidos y sorbo localizado.
- **Tramo de Tokio para editar ya subido:** media `1c3adc05-1a05-407c-a6a1-687be9259126` = vídeo 1 de 7,875 a 11,875 s (4,0 s, H.264 CRF 12, con audio). Los últimos 0,875 s son el plano siguiente: solo sirven de relleno (mínimo 4 s), se descartan al empalmar.
- **Prompts de edición redactados** por agentes en `prompts/revision_satoshi_prompts.json`: Tokio variante A (mira atrás por encima del hombro hacia la botella, 1,3–2,8 s del tramo) y B (susurra al hombre mirando la botella, 0,1–1,0 s); izakaya «main» (mano de mujer + brillo con `@Image1` = f1763dde) y «fallback» (añade el packshot `aade31ed-0151-469c-bc50-513aff07bb68` como lock). Son borradores: la revisión adversarial quedó a medias.
- Tareas abiertas en la sesión anterior: #15 gesto, #16 audio, #17 izakaya, #18 publicar.

Gastado en esta revisión: **0 créditos**. Tope propuesto para la revisión: **300 cr** (avisar al 50 % y al 80 %).

## 6. Lo que falta, en orden

1. **Revisión rápida de prompts** (sin créditos): leer `prompts/revision_satoshi_prompts.json`, comprobar contra la sección 4 y el lock de producto de `CLAUDE.md`. Seedance video_edit: el prompt describe el cambio, no la escena; `@Video1` / `@ImageN` en orden de subida; ≤3.900 caracteres.
2. **Tokio, gesto.** `generate_video` con `get_cost:true` y luego real: `model: seedance_2_5`, `mode: video_edit`, `resolution: 480p`, `generate_audio: false`, `medias: [{role: video_references, value: 1c3adc05-1a05-407c-a6a1-687be9259126}]`, `folder_id: af60db5b-3cf0-444c-8218-287a76fde27d`. Lanzar A y B (o A con `count: 2`). Coste esperado ≈ 12 cr por toma (se factura por la duración del vídeo fuente). QA: fotogramas cada 0,25 s de 0 a 3,125; el gesto se ve, la etiqueta intacta, el hombre igual, el corte a 3,125 sigue ahí. Máximo 2 reintentos, cambiando una sola variable.
3. **Izakaya, mano + brillo.** Mismo patrón: `seedance_2_5`, `video_edit`, `720p`, `generate_audio: false`, `medias: [{video_references: 66468164-b46b-41ab-a8c7-62554cc779ae}, {image_references: f1763dde-ff78-4fcb-8280-6ebf07b51d23}]` (+ `aade31ed-…` en el fallback). Coste esperado ≈ 56 cr por toma. QA: mano claramente femenina en 2,5–4,6 s, mismo tirón de cordón; tras el apagón solo brillan los contornos de las 4 siluetas y la manita, el texto y la cara amarilla oscuros, como en el vídeo 4; botella, tapón de rosca y etiqueta idénticos.
4. **Audio de Tokio (sin créditos).** Sobre la pista original completa de d45bbfb0, bajar el sorbo de 1,70 a 2,62 s unos −11 dB con rampas suaves, sin tocar el clink de 2,6 s. Punto de partida:
   ```
   ffmpeg -i d45bbfb0.mp4 -vn -af "volume='1-0.72*clip((t-1.70)/0.10,0,1)*clip((2.62-t)/0.06,0,1)':eval=frame" -c:a aac -b:a 192k audio_fix.m4a
   ```
   Si el sorbo sigue sonando «húmedo», añadir en esa ventana un `lowpass=f=3500`. Verificar con Whisper (que «Shushush» desaparezca o baje) y con el RMS. Después revisar 6–30 s por si hay más sorbos (sección 4).
5. **Empalme de Tokio.** `original[0–7,875] + editado[0–3,125] + original[11,0–30,05]`, 480×854, 24 fps, H.264 CRF 16, audio = `audio_fix.m4a`. Cortar en fotogramas exactos (7,875 s = fotograma 189; 11,0 s = fotograma 264). Comprobar que no hay salto de color en las uniones.
6. **Izakaya final.** Vídeo editado + **audio original** de 66468164 (`-map 0:v -map 1:a -shortest`), así se conserva el ambiente y la risa que gustaron. Comprobar duración (8,06 s) y sincronía del clic (3,6 s) y del apagón (5,4 s).
7. **Opcional, calidad de entrega.** Tokio está a 480p porque el draft caducó. Valorar `upscale_video` / `bytedance_video_upscale` (preset `aigc`) a 1080×1920 con `get_cost` antes; si es caro, entregar a 480p como lo vio el cliente y proponerlo aparte.
8. **Publicar.** mp4 y posters webp en `video/` y `poster/` (`v1_tokyo_30s_rev_satoshi.mp4`, `izakaya_mano_rev_satoshi.mp4`); ledger `prompts/revision_satoshi_jobs.json` con job ids, créditos reales y QA; `python3 tools/build_manifest_v1.py` (añadir las dos entradas nuevas si el script no las recoge); commit en español + push; actualizar la descripción de la PR #1. El dashboard de `sharp-zombie-review` se toca en otra sesión con solo ese repo.
9. **Mensaje para María**: borrador corto en español con qué se cambió en cada vídeo y los enlaces; el usuario lo reenvía.

## 7. Trampas conocidas

- La subida con `media_upload` exige en el PUT la cabecera `If-None-Match: *` además de `Content-Type`; sin ella da 400. Las URL firmadas caducan en horas: pedir una nueva si falla con `ExpiredToken`.
- En el sandbox, `showspectrumpic` de ffmpeg tarda más de 60 s y bloquea el sandbox («lifecycle busy»). Usar el script numpy con `nohup … &` y leer después.
- No usar `pkill -f` con patrones que aparezcan en el propio comando (mata la shell, salida 143).
- Seedance a veces sugiere el preset «IN THE DARK» en escenas oscuras: reenviar con `declined_preset_id: 24bae836-2c4a-48e0-89b6-49fcc0b21612`.
- Los ficheros del sandbox (`rev/cand/…`) pueden desaparecer si se recrea; volver a descargar desde las URLs de la sección 3.
- Commits terminan con las líneas de atribución que indique la sesión; nunca poner identificadores de modelo en commits ni PR.
