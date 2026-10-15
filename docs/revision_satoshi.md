# Revisión de Satoshi · 15-oct-2026

Cambios pedidos por Satoshi (socio de María, SWE) sobre los cuatro vídeos que vio, y cómo se han resuelto. Ledger con job ids, créditos y QA: `prompts/revision_satoshi_jobs.json`. Prompts: `prompts/revision_satoshi_prompts.json` (ronda 1) y el propio ledger (ronda 2).

## Resultado

| Vídeo | Petición | Qué se hizo | Final |
|---|---|---|---|
| 1 · Tokio «After Dinner» 30 s | Gesto de la mujer al retirar los platos; sorbo del brindis más suave | Seedance 2.5 `video_edit` sobre el tramo 7,875–11,875 s (2.º intento, job `7d494edf`): se detiene en la puerta, gira cabeza y hombros y mira hacia la botella (1,25–2,0 s del tramo). Sorbo bajado −11 dB (1,72–2,50 s, rampas 0,10/0,06 s) sin tocar el clink ni las risas. Empalme por fotogramas con el original | [`v1_tokyo_30s_rev_satoshi.mp4`](https://d2ol7oe51mr4n9.cloudfront.net/user_3BP9AlN7MxU50eaw9ZlO6ny5hI2/22829713-139e-4109-b5cf-5fec64c1a5e4.mp4) · 480×854, 30,05 s (misma resolución que el draft que vio el cliente) |
| 2 · Fiesta en casa 8 s | Ninguna | — | sin cambios |
| 3 · Izakaya, la mano apaga la luz 8 s | Mano de mujer; brillo de la etiqueta menos exagerado | Dos pasadas Seedance 2.5 `video_edit` a 720p: mano (job `72ad97b2`: dedos finos, uñas rosa nude, pulsera) y brillo (job `3ef4e359`, con el end frame del vídeo 4 como referencia: etiqueta oscura, solo contornos lima). Audio original (ambiente y risa) remuxado; apagón devuelto a 5,46 s | [`izakaya_mano_rev_satoshi.mp4`](https://d2ol7oe51mr4n9.cloudfront.net/user_3BP9AlN7MxU50eaw9ZlO6ny5hI2/cbf030e8-098c-47bc-9873-ca6ac7657757.mp4) · 720×1280, 8,06 s |
| 4 · Izakaya con copas 8 s | Ninguna (es la referencia de brillo) | — | sin cambios |

Créditos: 164 cr de un tope de 300 (ronda 1: 89 = 14 + 14 + 61; ronda 2: 75 = 14 + 61). Saldo Higgsfield: 1578,04 al inicio → **1375,04** al cierre (203 cr: 164 del pipeline, verificados en `transactions`, + 39 de generaciones de imagen hechas desde la cuenta a las 12:54–12:57 UTC, fuera de esta revisión).

## Qué falló y qué funcionó (lecciones)

- Seedance 2.5 `video_edit` a 480p devolvió la fuente **sin editar** (diff 3–5 niveles por fotograma) con los dos prompts largos de la ronda 1, dominados por frases de «conservar». Funcionó un prompt corto, con la acción primero y un gesto mayor (parada + giro de cabeza y hombros hacia cámara).
- A 720p editó la mano pero ignoró el cambio de brillo en el prompt combinado; dividir en dos pasadas (mano → brillo, usando el job de la mano como `@Video1`) resolvió el brillo a la primera.
- `video_edit` **retima**: el tramo de 96 fotogramas volvió con 89 y el corte se movió de f75 a f70. Se empalmó por fotogramas sin interpolar: original[0–188] + edit[0–69] + original[259–263] (cola estática) + original[264–720].
- Cada pasada de `video_edit` retrasó el apagón del izakaya un fotograma (f130→131 en la fuente, f132→133 tras dos pasadas). Corregido en post quitando dos fotogramas estáticos previos y clonando dos al final.
- Preflights `get_cost` y envíos: siempre con `declined_preset_id` de «IN THE DARK» (Seedance lo propone en las dos escenas).
- Coste real `video_edit`: 14 cr (4 s, 480p) y 61 cr (8 s, 720p). Alternativas preflighteadas y no usadas: Kling 3.0 Omni Edit 8 cr (4 s), Gemini Omni Flash 1.1 edit 27 cr (8 s, 720p).
- Los mp4 finales no se pueden traer al repo desde la sesión cloud (el proxy solo deja pasar github.com y raw.githubusercontent.com): se alojan en Higgsfield (`media_upload`) y `manifest.js` apunta a esas URL. Pósteres webp vía el puente `image_paths`.

## Borrador de mensaje para María (lo reenvía Bruno)

> Hola María, ya tenemos los dos vídeos con los ajustes de Satoshi:
>
> 1. **Tokio (30 s)**: al retirar los platos, ella se para un instante y mira hacia atrás, a la botella, como si hubiera notado algo. Y el sonido del sorbo del brindis va mucho más suave; el resto del audio queda igual.
>    https://d2ol7oe51mr4n9.cloudfront.net/user_3BP9AlN7MxU50eaw9ZlO6ny5hI2/22829713-139e-4109-b5cf-5fec64c1a5e4.mp4
> 2. **Izakaya, la mano que apaga la luz (8 s)**: la mano ahora es de mujer y el brillo de la etiqueta a oscuras es como en el vídeo de las copas, solo los contornos.
>    https://d2ol7oe51mr4n9.cloudfront.net/user_3BP9AlN7MxU50eaw9ZlO6ny5hI2/cbf030e8-098c-47bc-9873-ca6ac7657757.mp4
>
> Los otros dos (la fiesta en casa y las copas) se quedan como están. El de Tokio va a la misma resolución que viste; si os convence, lo pasamos a 1080p para la entrega final.
>
> Una cosa: el comentario de Satoshi me llegó cortado («se nota un poco que los vídeos están…»). ¿Me pasas el final por si pide algo más?

## Pendiente

- Dashboard `sharp-zombie-review`: comprobar que muestra la línea nueva `E_REV_SATOSHI` (escenas TOKIO e IZAKAYA) de `manifest.js`; se toca en una sesión aparte con solo ese repo.
- Opcional: upscale de Tokio a 1080×1920 (`upscale_video`, proveedor bytedance, preset `aigc`, fuente = media `22829713-139e-4109-b5cf-5fec64c1a5e4`, 480×854); no admite preflight de coste.
- Si se quieren los mp4 en `video/`: descargarlos en local desde las dos URL y hacer commit (`video/v1_tokyo_30s_rev_satoshi.mp4`, `video/izakaya_mano_rev_satoshi.mp4`); el manifest puede seguir apuntando a Higgsfield.
