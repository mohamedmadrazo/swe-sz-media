---
name: comercial-pipeline
description: Pipeline Streamline3X para comerciales de 30 s o más (Sharp Zombie y clientes futuros): guion → referencias en sucio con Higgsfield → diseño del set en Blender × Higgsfield (3D Jutsu + bpy) → rodaje (cámara virtual, móvil del usuario como driving video de Genjutsu, animatic Seedance) → postproducción en Premiere. Usar siempre que el usuario pase un guion, pida un spot/comercial/vídeo de producto, hable de referencias, previz, rodaje, Genjutsu, Restyle, keyframes, storyboard o postpro. Carga docs/pipeline_comercial.md y sigue sus fases y puertas.
---

# Pipeline comercial (loop)

1. Lee `docs/pipeline_comercial.md` (procedimiento completo, puertas G1–G4, costes, lecciones) y `CLAUDE.md` (ids, locks, reglas del repo).
2. Carga las skills `anthropic-skills:higgsfield-prompt-director`, `anthropic-skills:higgsfield-genjutsu` y `anthropic-skills:senior-tool-prompter` antes de escribir prompts.
3. Ejecuta las fases en orden; no saltes a vídeo sin referencias aprobadas; usa Workflow de agentes (redacción → lint → generación → QA 3 lentes con veto de producto) en lotes grandes.
4. Mantén ledgers JSON (`prompts/*_jobs.json`), regenera `docs/*_assets_ledger.md` y `manifest.js` con los scripts del repo, y haz commit + push + PR borrador al cerrar cada fase.
5. Informe al usuario al final de cada fase: qué hay, créditos reales (`balance`), qué decidir en la siguiente puerta.
