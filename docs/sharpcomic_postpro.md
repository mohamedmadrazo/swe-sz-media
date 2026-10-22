# SHARPCOMIC · postproducción del spot cómic · 22-oct-2026

Spot de cómic pop-art de Sharp Zombie (16:9) a partir de tres generaciones de Higgsfield del 11-jul que Bruno había montado en Premiere sin terminar. Ledger completo con job ids, EDL y medidas: `prompts/sharpcomic_jobs.json`.

## Qué se ha hecho

| Paso | Resultado |
|---|---|
| Upscale | Los tres clips a 1920×1080 (bytedance `aigc`), frame a frame idénticos a las fuentes. |
| Secuencia nueva | `SHARPCOMIC_MASTER_1080` en el proyecto `SHARPCOMIC.prproj` (bin `SHARPCOMIC_1080_master`). La secuencia original de Bruno sigue intacta. |
| Unión 1 (11,17 s) | El final de c1 y el arranque de c2 son el mismo encuadre (ECC 0,99): fundido de 12 frames con la cola de c1 en V2 y cola de audio de c1 en A2, que tapa los 0,25 s de silencio con que empieza c2. |
| Unión 2 (26,21 s) | Punch de salida en c2 (100→118 %), destello blanco de 5 frames con el pico en el corte, punch de entrada en c3 (112→100 %) y el silbido del lanzamiento entrando 0,54 s antes por A2. |
| Producto | Fuera el giro del lanzamiento (c3 f68–81), donde la etiqueta salía en espejo; c3 entra directamente en el «SPLAT». El resto de planos de producto se revisaron y están bien. |
| Clip final (4 s) | Kling 4.0 con fotograma inicial (último de c3) y final (GPT Image 2.5 sunburst): se apaga la luz y solo brillan en lima los contornos de las siluetas; la etiqueta queda oliva oscuro y «Sharp Zombie» rojo oscuro legible. Encadenado con 4 frames de fundido. |
| Sonido | Clips igualados a ~−21,4 LUFS; máster a **−14,0 LUFS, −1,6 dBTP, LRA 7,7** en A3 (A1/A2 silenciadas pero editables). |
| Export | En cola de Media Encoder: `SHARPCOMIC_MASTER_1080p.mp4` en la carpeta del proyecto. |

Duración final: 41,71 s (1001 frames, 24 fps). Créditos: 19,81 (saldo 816,94 → 797,13).

## Lecciones (conector Premiere en el equipo de Bruno, Premiere en español)

- Los nombres de efectos y propiedades van **localizados**: `Movimiento` (`Posición`, `Escala`, `Punto de anclaje`), `Opacidad`, `Volumen` → `Nivel`. `pr_add_audio_fade` y `pr_set_audio_level` fallan porque buscan «Level»; usar `pr_add_keyframe`/`pr_set_effect_property` sobre `Volumen`/`Nivel`.
- `Nivel` es lineal: valor = 10^((dB − 15)/20) (0 dB = 0,17783; −40 dB = 0,0017783).
- `Posición` y `Punto de anclaje` son 2D: `pr_add_keyframe` solo admite números, así que no se puede animar un zoom dirigido a un punto; solo escala desde el centro.
- Transiciones nativas por QE: fallan («every addTransition form threw»); construirlas con keyframes de opacidad (receta I del skill).
- `pr_apply_effect('Hard Limiter')` responde `applied:true` pero no aplica nada en audio.
- La cola de Media Encoder conserva trabajos de otros proyectos: al pulsar «Iniciar cola» el 22-oct se renderizó primero un trabajo antiguo de Bakari. Antes de encolar, revisar la cola o exportar desde Premiere.
- Exportar: `pr_export_sequence`, `pr_extract_audio` y `pr_export_sequence_frame` no producen archivo en esta instalación; `pr_add_to_render_queue` con un `.epr` explícito sí encola en AME. `pr_export_frame` funciona solo hacia una carpeta existente (y añade `.png` si la ruta ya lo lleva).
- `pr_upload_media` rechaza PNG (400): la QC visual se hace sobre vídeo exportado o en el sandbox.
- `pr_import_media` con tres URLs de ~20 MB agota el puente: importar de una en una. Los ficheros quedan en `AppData\Local\Temp\higgsfield-ae-bridge`: recopilar con el Gestor de proyectos antes de limpiar Temp.
- `pr_apply_cut_plan` con `track:"A"` también coloca el vídeo enlazado en V2: borrarlo justo después.
- Los puntos de entrada caen un frame antes si el valor es exactamente n/24 (2,583333 → f61): pasar n/24 + 0,0015.
- Seedance 2.5 falló sin motivo (reembolsado). Kling 4.0 con solo `start_image` inventa el brillo (toda la etiqueta); con `start_image` + `end_image` hecho en GPT Image el brillo sale fiel al producto y cuesta 4 cr a 1080p.

## Pendiente

- Exportar el máster cuando Bruno lo pida, desde Premiere (Archivo → Exportar → Medios, H.264 «Coincidir con origen – Velocidad de bits alta») y no por la cola de AME, y hacer la QC del MP4 final (frames en las uniones y sonoridad). El trabajo encolado por API el 22-oct no llegó a generar archivo.
- Recopilar medios del proyecto (Archivo → Gestor de proyectos) para sacar los clips 1080p de la carpeta temporal.
- Opcional: variante 9:16 para Reels (reencuadre por plano).
