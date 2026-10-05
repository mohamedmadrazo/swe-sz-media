# Brief para GPT-6 Astra (Supercomputer) — revisión de prompts · Sharp Zombie · Vídeo 1 "After Dinner, Tokyo"

> Cómo usarlo: en Higgsfield **Supercomputer** → selector de modelo → **GPT-6 Astra**. Pega este documento completo y, debajo, el JSON de `prompts/video1_prompts.json` (o solo los paquetes que quieras revisar). Pídele: *"Revisa cada prompt contra los locks y la gramática del modelo indicado; devuelve, por asset_id, (a) fallos detectados, (b) prompt corregido completo, (c) un cambio de una sola variable para el siguiente reintento si el resultado fallara"*. Devuélveme sus sugerencias y las integro.

## 1. Qué es esto
Spot de 15 s (9:16, variante 16:9), sin diálogo, solo música. Una pareja japonesa (Aya y Ren) termina de cenar a la luz de la luna en un apartamento de Tokio; recogen los platos; se apaga la luz; las siluetas de la etiqueta de **Sharp Zombie (Rioja D.O.Ca.)** brillan, cobran vida, bailan, trepan por las copas y acaban borrachas en el vino. Look: preset **"Neon Graphic Cinematic 3D"** (Genjutsu Restyle): 3D estilizado con sombreado de cómic, tramas halftone, líneas de tinta, desregistro cromático sutil, luces de borde magenta/cian sobre azul noche.

## 2. Locks (deben aparecer literalmente en los prompts)
- **PRODUCT_LOCK_NB** (Nano Banana Pro / Kling, con Element `@SZ-bottle-master`): "The bottle is exactly @SZ-bottle-master: dark glass Bordeaux bottle, black screw cap, bright yellow front label framed top and bottom by black-and-yellow diagonal caution stripes, four black zombie silhouettes in a row (three lurching zombies in profile with bent, raised arms in a staggering zombie walk and one crouched) plus a small black hand rising from the ground, the name in dark red gothic blackletter and the word RIOJA below it. Keep the label geometry, colours, stripes and silhouettes exactly as the reference; ignore the reference's white background. The cap is a screw cap, never a cork."
- **PRODUCT_LOCK_GPT** (GPT Image 2.5 / Seedream / Seedance, con el packshot como Image 1): "Image 1 is the product: preserve the bottle shape, the black screw cap, the yellow label, the black-and-yellow caution stripes, the four black zombie silhouettes (three lurching in profile with bent raised arms, one crouched) and the small rising hand, the dark red blackletter name and the RIOJA line exactly as shown. Ignore Image 1's white background. Do not redraw, restyle or re-letter the label."
- **GLOW_LOCK** (escenas a oscuras): "In the dark only the thin outlines of the four zombie silhouettes and the small hand glow a soft phosphorescent lime-green (thin luminous edge, gentle falloff, no neon tube look, no bloom halo, no lens flare), exactly like the real photo. The label text and stripes do not glow; the yellow label reads as dark grey-green in the dark."
- **STYLE_LOCK**: "Image S defines the visual style only — stylized 3D animation with graphic comic-book shading, halftone dots in the shadows, bold ink edge lines, subtle misregistered colour fringes, neon magenta and cyan rim lights over deep night blues, cinematic depth of field — do not copy its content, characters or layout. The bottle label stays accurate and readable."
- **EXCLUSIONS_COMMON**: "no extra bottles, no cork, no candles, no readable captions or added text, no logos other than the label, no watermark, no neon signs with brand names, no extra fingers, no plastic skin, no faces or eyes on the zombie silhouettes, no purple lens flares."
- Zombies fuera de la botella: ~5 cm, silueta negra mate con contorno lima fino, **sin ojos ni boca**.

## 3. Beats (24 fps, 0–360)
| Beat | s | Acción | Cámara |
|---|---|---|---|
| 1 | 0.0–2.5 | Sobremesa, risas, última copa, luna | Travelling 35 mm desde la entrada |
| 2 | 2.5–4.0 | Gato cruza y mira a cámara (EE1) | sigue |
| 3 | 4.0–5.5 | Se levantan con los platos y salen por la derecha; quedan botella, tapón, copas | se detiene a 1 m, 50 mm |
| 4 | 5.5–6.5 | **Corte.** Apagón; luna azul | push-in 50→85 mm |
| 5 | 6.5–8.5 | Macro etiqueta: contornos laten; el agachado duerme (EE2); música desde 7.5 s | macro 100 mm |
| 6 | 8.5–10.5 | **Corte.** Se despegan y bajan bailando; la mano anda con los dedos (EE3) | nivel mesa, tracking |
| 7 | 10.5–12.0 | Limbo bajo palillos (EE4), DJ con tapón (EE5), estatuas al pasar la sombra de Ren (EE6), maneki-neko (EE7) | tracking + arc |
| 8 | 12.0–13.5 | Escalada por los tallos, caen al vino; la mano cuelga | tilt-up 85 mm |
| 9 | 13.5–15.0 | Borrachera; gato asoma; plano final botella + copas | pull-back, hold |

## 4. Gramática por modelo (lo que Astra debe comprobar)
- **nano_banana_pro**: frases completas, marco positivo; Elements como `@nombre` (en la API, `<<<uuid>>>`), nunca en medias; ≤8 refs; primera referencia = clave de estilo S.
- **gpt_image_2_5**: brief USE / STYLE / SCENE / SUBJECT / REFERENCES / CAMERA / CONSTRAINTS; `Image N` en el orden de las medias; `quality:"high"`; variante `sunburst` solo para "change only X" sobre una imagen base; `flare` para composición nueva.
- **seedream_v5_pro**: descripción limpia; textos exactos entre comillas; tipografía descrita.
- **seedance_2_5** (vídeo): secciones GLOBAL STYLE / ACTIVE REFERENCES (@Image N) / SCENE / FIRST FRAME AND BLOCKING / `SHOT n | t0 to t1 |` / PHYSICS / STILLNESS LOCK / AUDIO con `(música)`; cortes duros en 5.5 y 8.5 s; `draft:true`.
- **kling3_0**: `Shot 1 (3s):` ≤5 shots ≥3 s; 80 % idéntico entre shots; Element solo con `start_image`; `sound:"off"`.
- **Genjutsu (hf_mult_motion_control)**: plantilla MOTION TRANSFER (@Video1 driving, @Image1 LEAD, @Image2 LOCATION, locks, `Avoid:`), ≤3.900 caracteres.

## 5. Qué pedirle a Astra exactamente
1. Para cada paquete: ¿están los locks literales? ¿gramática correcta? ¿pide texto legible donde no debe? ¿describe caras/ojos en zombies? ¿corcho? ¿escala 5 cm?
2. ¿El prompt cuenta el beat correcto (tiempo, cámara, easter egg)?
3. Un prompt corregido completo por paquete + un cambio de UNA variable como plan B.
4. Para los prompts de vídeo (Seedance/Kling/Genjutsu): riesgos de deriva de etiqueta y cómo mitigarlos en el texto.
