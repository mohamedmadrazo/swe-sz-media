# HANDOFF · Revisión de Satoshi · 15-oct-2026 (cierre de la sesión 2)

Documento de traspaso entre sesiones. Leerlo entero antes de tocar nada. El detalle de la revisión está en `docs/revision_satoshi.md` y el ledger en `prompts/revision_satoshi_jobs.json`.

## 0. Cómo arrancar la sesión nueva

- Repo `mohamedmadrazo/swe-sz-media`, rama `claude/youthful-hawking-b0e6vw` (apilada sobre `claude/confident-goldberg-rw44ia`, PR #1). Con un único repo la sesión lee `.claude/settings.json` (permisos para python3, ffmpeg, git, curl, Higgsfield, GitHub). Modo **Auto**.
- Higgsfield: workspace `6f3d1bc8-8c68-4180-a5b0-9582e2da64ea`; carpeta del vídeo 1 `af60db5b-3cf0-444c-8218-287a76fde27d`.
- Red: el proxy bloquea cloudfront y higgsfield.ai; el trabajo de medios va en `sandbox_exec` (ffmpeg, Pillow, numpy, faster-whisper). Ver imágenes con `image_paths` (máx. 4, ≤512 KiB); las que vuelven se guardan en local (puente válido para pósteres).

## 1. Hecho en esta sesión (15-oct)

- **Tokio 30 s**: gesto de la mujer (Seedance 2.5 `video_edit`, 2.º intento, job `7d494edf`) + sorbo −11 dB + empalme por fotogramas → `v1_tokyo_30s_rev_satoshi.mp4` alojado en Higgsfield, media `22829713-139e-4109-b5cf-5fec64c1a5e4` (480×854, 30,05 s, 721 fr).
- **Izakaya mano**: mano de mujer (job `72ad97b2`) + brillo natural (job `3ef4e359`) + audio original, apagón corregido → `izakaya_mano_rev_satoshi.mp4`, media `cbf030e8-098c-47bc-9873-ca6ac7657757` (720×1280, 8,06 s, 193 fr).
- Créditos gastados: **164 cr** (tope 300); saldo real al cierre **1375,04** (además, 39 cr de imágenes generadas desde la cuenta fuera del pipeline). Ledger, QA y lecciones en `docs/revision_satoshi.md`.
- `manifest.js` regenerado con `tools/build_manifest_v1.py` (ahora también lee `prompts/revision_satoshi_jobs.json` → línea `E_REV_SATOSHI`, 2 entradas); pósteres `poster/v1_tokyo_30s_rev_satoshi.webp` y `poster/izakaya_mano_rev_satoshi.webp`.
- Los mp4 finales **no están en `video/`** (el proxy de la sesión cloud no deja descargarlos); el dashboard y el cliente usan las URL de Higgsfield.

## 2. Lo que falta, en orden

1. Bruno reenvía a María el borrador de mensaje de `docs/revision_satoshi.md` (con los dos enlaces) y le pide el final del comentario cortado de Satoshi.
2. Dashboard `sharp-zombie-review` (otro repo, sesión aparte con solo ese repo): comprobar que la línea `E_REV_SATOSHI` con escenas `TOKIO` / `IZAKAYA` se muestra; si el dashboard filtra por líneas conocidas, añadirla.
3. Si el cliente aprueba: upscale de Tokio a 1080×1920 (`upscale_video` bytedance, preset `aigc`, fuente media `22829713-…`, 480×854, 24 fps). Sin preflight de coste: mirar `balance` antes y después.
4. Opcional: traer los mp4 al repo desde un equipo local (descarga de las URL + commit en `video/`).
5. Vídeos 2 (fiesta) y 4 (copas): sin cambios, no tocar.

## 3. Trampas conocidas

- Seedance `video_edit`: a 480p con prompts largos de «conservar» devuelve la fuente sin editar; usar prompt corto, acción primero, gesto grande. Para dos cambios, dos pasadas (la segunda con el job de la primera como `@Video1`).
- `video_edit` retima (96 → 89 fr) y mueve el corte; comprobar el fotograma del corte con luminancia y empalmar por fotogramas. Cada pasada retrasa el apagón un fotograma.
- Seedance propone el preset «IN THE DARK» en estas escenas: siempre `declined_preset_id: 24bae836-2c4a-48e0-89b6-49fcc0b21612`, también en los `get_cost`.
- `media_upload`: el PUT exige `If-None-Match: *` y `Content-Type`; copiar la URL firmada tal cual (un carácter cambiado → 400). Las URL caducan en 24 h.
- `showspectrumpic` de ffmpeg bloquea el sandbox (>60 s): espectrogramas con numpy + Pillow.
- No usar `pkill -f` con patrones que aparezcan en el propio comando.
- Los ficheros del sandbox (`rev/…`) pueden desaparecer; las fuentes se re-descargan de las URL del ledger.
- Commits terminan con las líneas de atribución que indique la sesión; nunca poner identificadores de modelo en commits ni PR.
