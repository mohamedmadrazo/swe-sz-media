# Cómo aplicar el preset "Neon Graphic Cinematic 3D" (Genjutsu Restyle) al vídeo 1

Verificado el 4-oct-2026 contra el changelog de Higgsfield (entrada del 30-sep-2026 "Genjutsu Restyle") y la documentación de la API pública.

**Qué es:** Genjutsu Restyle redibuja un vídeo completo en un estilo visual preajustado conservando movimiento, timing, cámara y audio fuente. Funciona en modo *Motion transfer*; vídeo guía de 4–30 s; hasta 5 imágenes de referencia de personajes (API) / 30 (web); salida 480p/720p/1080p (hereda el ratio del vídeo guía).

**Vídeo guía recomendado:** `video/v1_previz_3djutsu.mp4` (previz 3D a escala real, 15 s, 9:16) o el draft Seedance `v1_vid_01`. **Referencias de personaje:** sheets neutras de Aya y Ren (`v1_char_01n`, `v1_char_02n`), sheet de zombies (`v1_char_04`), packshot de la botella (`aade31ed`).

## Vía 1 — API pública (oficial)

```bash
# 1) catálogo de estilos (requiere API key de open.higgsfield.ai; guardar como secretos HF_API_KEY_ID / HF_API_KEY_SECRET)
curl -sS 'https://api.higgsfield.ai/models/higgsfield/genjutsu/restyle/v1.0/presets' \
  -H "Authorization: Key ${HF_API_KEY_ID}:${HF_API_KEY_SECRET}" | jq '.items[] | select(.name|test("Neon Graphic";"i"))'
# 2) generar (preset_id = UUID del estilo "Neon Graphic Cinematic 3D")
curl -sS -X POST 'https://api.higgsfield.ai/higgsfield/genjutsu/restyle/v1.0' \
  -H "Authorization: Key ${HF_API_KEY_ID}:${HF_API_KEY_SECRET}" -H 'Content-Type: application/json' \
  --data '{"video_url":"<URL pública del vídeo guía>","preset_id":"<UUID>","image_urls":["<aya>","<ren>","<zombies>","<botella>"],
           "prompt":"Preserve the original camera movement and timing. The bottle keeps its exact yellow caution-stripe label, dark red blackletter name, RIOJA line, four black zombie silhouettes and small hand, black screw cap. Only the silhouette outlines glow lime-green in the dark. Keep the couple and the calico cat consistent across shots.",
           "resolution":"480p"}'
# 3) sondear status_url hasta "completed" y descargar video.url
```
Precio aproximado: $0.318 / $0.681 / $1.632 por segundo (480p / 720p / 1080p) — se factura en USD, no en créditos del plan.

## Vía 2 — Web (manual)
Higgsfield → Video → Genjutsu → **Styles** → elegir "Neon Graphic Cinematic 3D" → subir el vídeo guía + las referencias → Generate (480p primero, 1080p al aprobar).

## Vía 3 — MCP (aproximación, verificar con smoke test)
`generate_video` con `hf_mult_motion_control` acepta `preset_id` en los parámetros preparados sin error (preflight de coste OK: 18 cr por 7 s a 480p), pero no está confirmado que el backend aplique el preset. El test `v1_vid_03` (5 s, 480p) lo confirma. Si no lo aplica: estilo por referencia — añadir el style key (`v1_env_01`, job `30a2a515…`) como @Image y un bloque `STYLE:` en el prompt de motion transfer.

## Lock de producto para cualquier vía
Etiqueta amarilla con franjas caution negro/amarillo, "Sharp Zombie" en gótica rojo oscuro, RIOJA, D.O.Ca., cuatro siluetas negras (tres caminando brazos al frente + una agachada) y manita, tapón de rosca negro. En oscuridad solo brillan los contornos (verde lima fino, sin neón ni bloom); el texto no brilla.
