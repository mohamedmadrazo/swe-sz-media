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

## Audio v2 y máster MP4 (22-oct, petición de Bruno: «bajar y arreglar el audio»)

- Problemas medidos: 0,65 s de silencio digital tras el «SPLAT» con entrada de golpe de la banda grave en la zambullida; «SPLAT» muy agudo; rescate y final casi solo subgrave; máster a −14 LUFS apretado.
- Arreglos: ambiente muy bajo en el hueco, «splat» invertido como subida hasta el corte de la zambullida, campana −3,5 dB a 3,5 kHz en el «SPLAT», low-shelf −4 dB a 75 Hz desde la zambullida, paso alto 30 Hz, máster a **−16,0 LUFS / −1,9 dBTP / LRA 9,0**. Sustituido en A3 de Premiere.
- El MP4 no sale por la API de Premiere ni por la cola de AME en esta instalación: el máster se renderiza en el sandbox replicando la secuencia fotograma a fotograma (`render_master.py`) y se entrega por enlace en `entregables/2026-10-22_sharpcomic/`.

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

- Máster entregado el 22-oct (render en el sandbox). Si se quiere una copia exportada por el propio Premiere en `05_entregables`: Archivo → Exportar → Medios con la secuencia activa.
- Recopilar medios del proyecto (Archivo → Gestor de proyectos) para sacar los clips 1080p de la carpeta temporal.
- Opcional: variante 9:16 para Reels (reencuadre por plano).

## Retoque del cliente (27/28-oct): cartel «Sharp» y etiqueta real

Petición: el panel derecho del cartel de la tienda decía «ZONBR!» y debía decir «Sharp»; las siluetas de la etiqueta incluían una chica y debían ser las reales (tres zombis andando de perfil, uno agachado y la manita). Bruno pidió no gastar créditos si salía caro: se ha hecho todo por composición, **0 créditos**.

- **Cartel** (fr 20–92): el panel derecho se sigue con homografías SIFT encadenadas desde el fotograma 88 y suavizadas; dentro se pega el «SHARP» del panel izquierdo rectificado y recoloreado al magenta del panel derecho, con fondo blanco del propio panel. La farola que pasa por delante se respeta con una máscara.
- **Etiqueta**: por plano, se elige un fotograma de referencia, se rectifica la etiqueta (rectángulo mínimo de la zona amarilla con texto rojo), se borra la banda de figuras desde justo debajo de «Zombie» hasta el suelo con el amarillo vecino y se pegan las siluetas reales (`3d/textures/label_silhouettes_fill.png`, sin los restos de borde). Ese parche se lleva a cada fotograma con homografías SIFT encadenadas, con corrección de ganancia de color y respetando los dedos (máscara de piel por blobs grandes). En el apagón final las siluetas nuevas llevan contorno lima con glow, como el resto del cierre.
- En la caída y el giro de la botella (26–34 s), demasiado rápidos para seguir con homografía, la etiqueta se detecta y rectifica fotograma a fotograma.
- Sin tocar: la pelea (6,4–9,8 s) y el salto (18–21 s), donde la botella es diminuta o va de espaldas, y los fotogramas del destello del SPLAT.
- Audio: el del máster v2, sin cambios.
- Máster v3: `entregables/2026-10-22_sharpcomic/ENTREGA.md`.

Lecciones:
- El pelo amarillo de la chica se funde con la etiqueta en la segmentación por color: elegir la componente con texto rojo (fracción roja 4–40 %), no la mayor.
- La máscara de piel coge los bordes antialiasados de las figuras negras sobre amarillo (tono ≈18): quedarse solo con blobs grandes (>600 px) o salen motas de las figuras viejas.
- La banda de figuras sobresale por debajo del rectángulo amarillo (piernas sobre el suelo negro): ampliar el lienzo rectificado por abajo (`pb`) y, en etiquetas al revés, no ampliarlo (el volteo desplaza la banda sobre el texto).

## Retoque del cliente (29-oct): vuelta a la etiqueta original, cartel y versión corta

- Bruno descartó la v3 (siluetas de la etiqueta cambiadas): se vuelve al máster v2 con la etiqueta original.
- Cartel «ZONBR!» → «SHARP» rehecho y llevado a Premiere como clip en V3 de `SHARPCOMIC_MASTER_1080` (0,83–3,88 s). Lecciones: el color de relleno a la derecha del parche no puede salir de una mediana de columnas que toque la «P» (dejaba una marca); el borde derecho se limita por fotograma al marco rosa; la farola que pasa por delante se sigue con su propia trayectoria (detector de franja gris + interpolación), porque la detección por columnas oscuras daba falsos positivos en los fotogramas borrosos.
- La extensión no exporta fotogramas de la secuencia (`exportFramePNG produced no file`): la comprobación visual se hizo sobre el composite equivalente en el sandbox; el clip en V3 está a escala 100 % y posición 0,5/0,5, igual que u1.
- Versión corta (pedido de Bruno): fuera 12:20–26:04; el corte une la misma pose de la chica y entra en el destello del «SPLAT». 28,4 s, −16 LUFS. Secuencia `SHARPCOMIC_MASTER_1080_v5_corto`. Enlaces en `entregables/2026-10-22_sharpcomic/ENTREGA.md`.
