# swe-sz-media — assets de Sharp Zombie (SWE) · Streamline3X

Repositorio de assets servido en GitHub Pages (`manifest.js` alimenta el dashboard `sharp-zombie-review`). Trabaja en español; commits en español.

## Procedimiento
- Para cualquier comercial/spot: invoca la skill `comercial-pipeline` y sigue `docs/pipeline_comercial.md` (fases, puertas G1–G4, costes, lecciones aprendidas).
- Vídeo 1 "After Dinner, Tokyo": biblia `docs/video1_bible.md`, storyboard `docs/video1_storyboard.md`, ledger `docs/video1_assets_ledger.md`, preset Restyle `docs/video1_restyle_howto.md`.

## Ids fijos (Higgsfield)
- Carpeta de proyecto: `af60db5b-3cf0-444c-8218-287a76fde27d`.
- Elements: SZ-bottle-master `de0c221b-6bd9-4ab5-912b-c6840b2423cc` · SZ-bottle-back `29cbd6df-d8cd-405f-aa0a-3974b6cfb28c` · SZ-aya `65a0c653-c433-4c10-a435-a4ce5504f0a2` · SZ-ren `c800522c-a722-4f47-bb45-2f32899d7e45` · SZ-zombies-glow `5915e7ac-09c7-4efc-bf78-a1904ace295b` · SZ-cat `2ab36fde-48a2-4f46-ba0c-0e3c66e86f84` · SZ-apartment `0199fa74-cff0-459d-801c-fae3153bf8bd`.
- Refs: packshot `aade31ed-0151-469c-bc50-513aff07bb68`, foto real glow `a1c24793-cf2e-4f5b-8b0f-4e69b82bbbfa`, clave de estilo S (iluminada) `30a2a515-405f-41f1-b785-2456b943d14d`; **look definitivo = fase oscura** (KF6 `94052ac7-c2c1-41c9-a7ff-1340c8b5e82d`, KF7 `fdead37f-5f7c-4afe-88d8-3ce13f5aa905`).
- 3D Jutsu "Tokyo apt previz V1": `0d680169-83bc-4288-b579-1101122d639e` (rev 2).

## Producto (lock)
Botella Bordeaux de vidrio oscuro, **tapón de rosca negro** (nunca corcho), etiqueta amarilla con franjas caution negro/amarillo arriba y abajo, "Sharp Zombie" en blackletter rojo oscuro, RIOJA, Denominación de Origen Calificada, cuatro siluetas negras (**tres en marcha zombi de perfil con brazos doblados y levantados, una agachada**) y una manita; a oscuras solo brillan los contornos en verde lima fino (el texto no). Contraetiqueta real: `3d/textures/label_back.png`.

## Reglas técnicas
- Blender local solo CYCLES CPU (Eevee/Workbench abortan: sin libEGL); renders largos con nohup y log `[FRAME]/[DONE]`; para matar procesos `pgrep -f "^python3 <script>"` (nunca `pkill -f` con patrones genéricos).
- 3D Jutsu: una mutación por vez con guards frescos; vídeo solo con Workbench (Eevee ≈20 s/frame, límite 300 s por op).
- Importar al Higgsfield desde el repo: mp4 vía `https://cdn.jsdelivr.net/gh/mohamedmadrazo/swe-sz-media@<sha>/...`, png vía `raw.githubusercontent.com` (el proxy local bloquea cloudfront/higgsfield.ai; ver con `sandbox_exec image_paths`).
- Manifest: `python3 tools/build_manifest_v1.py` (nunca a mano); ledger: `python3 prompts/build_ledger_md.py`; storyboard: `python3 prompts/build_storyboard_md.py`.
- No subir carpetas de renders PNG (`3d/.gitignore`); sí webp/mp4 en `img/`, `poster/`, `video/`.
- Drafts Seedance `draft:true` caducan a los 7 días: anotar `expires` en `prompts/video_jobs.json`.
