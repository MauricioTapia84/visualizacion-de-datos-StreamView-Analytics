# Documentación Markdown — Convenciones

Esta carpeta almacena todos los archivos Markdown generados como entregables, análisis y documentación producida por agentes o por colaboradores humanos.

Reglas principales
- Ubicación obligatoria: `documentation/markdown/`.
- Nomenclatura recomendada:
  - Entregables de evaluación: `EP{n}_<descripción>.md` (ej.: `EP1_informe_ejecutivo.md`).
  - Análisis ad-hoc: `analysis_<tema>.md` (ej.: `analysis_popularidad_generos.md`).
  - Registro de adaptaciones de agentes: `agents_adaptation_log.md`.
- Cada archivo debe comenzar con un bloque YAML con estos metadatos mínimos:

```yaml
---
title: "Título descriptivo"
author: "Nombre del autor o agente"
date: 2026-08-27
source_files:
  - notebooks/analisis.ipynb
  - src/utils.py
---
```

- Incluir un resumen ejecutivo (máx. 6 líneas) inmediatamente después del bloque YAML.
- Si el documento contiene código o resultados reproducibles, añadir una sección `Reproducibilidad` con comandos y dependencias.

Buenas prácticas
- Mantener lenguaje técnico y conciso en español.
- Enlazar a datasets en `data/` usando rutas relativas.
- Añadir referencias a secciones del caso semestral cuando corresponda.

Ejemplo mínimo (estructura):

- YAML metadata
- Resumen ejecutivo
- Contexto y objetivos
- Metodología / pasos realizados
- Resultados (gráficos, tablas)
- Conclusiones y recomendaciones
- Reproducibilidad (comandos, entorno)

Si quieres, creo plantillas `EP1_template.md` y `analysis_template.md` en esta carpeta. Indícame si quieres que las genere ahora.