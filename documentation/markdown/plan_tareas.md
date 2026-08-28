---
title: "Plan paso a paso y cronograma para completar el proyecto"
author: "Equipo StreamView (asistente)"
date: 2026-08-27
source_files:
  - documentation/markdown/plan_tareas.md
---

Resumen ejecutivo

Este plan divide el proyecto en 4 etapas alineadas con EP1..EFT y desglosa tareas detalladas, entregables y dependencias. Estimaciones temporales son orientativas; ajustar según disponibilidad.

Fase 0 — Preparación (1–2 días)
- T0.1: Crear entorno: virtualenv + `requirements.txt` (pandas, numpy, matplotlib, seaborn, plotly, altair, geopandas opcional, streamlit/plotly dash si se usa). 
- T0.2: Estructurar repositorio (si falta) y confirmar datasets en `data/`.
- Entregable: `documentation/markdown/README.md` (ya creado), checklist inicial.

Fase 1 — Comprensión del negocio y exploración visual (EP1) (5–7 días)
- T1.1: Revisión de la rúbrica y caso (documentado).
- T1.2: Auditoría de calidad de datos (nulos, duplicados, tipos) y registro en MD.
- T1.3: Limpieza mínima reproducible (fechas, country, genres). Guardar script/notebook en `notebooks/` y referenciar en MD.
- T1.4: EDA: KPI básicos (totales, por género, país, idioma), primeras visualizaciones (barras, treemap, series temporales).
- T1.5: Redacción de informe ejecutivo EP1 con storytelling (resumen, hallazgos, 3 recomendaciones). 
- Entregables EP1: `EP1_informe_ejecutivo.md`, notebooks y figuras en `images/`.

Fase 2 — Diseño e implementación de dashboards (EP2) (10–15 días)
- T2.1: Definir requerimientos de dashboard por audiencia (Directorio, Contenidos, Marketing).
- T2.2: Wireframes y prototipos (mockups simples). Documentar decisiones.
- T2.3: Implementación técnica: elegir stack (Plotly Dash / Streamlit / Power BI). 
- T2.4: Construcción de KPIs y vistas interactivas (filtros, navegación, export CSV).
- T2.5: Test de usabilidad rápida y ajustes.
- Entregables EP2: Dashboard funcional (link/archivo), `EP2_dashboard_documentation.md`.

Fase 3 — Evaluación y optimización (EP3) (5–7 días)
- T3.1: Recolección de feedback y métricas de uso.
- T3.2: Refinamiento visual (paletas accesibles, etiquetas claras).
- T3.3: Revisión de consistencia y justificación técnica por visual.
- T3.4: Informe crítico con mejoras y comparaciones antes/después.
- Entregables EP3: `EP3_evaluacion.md`, versión mejorada del dashboard.

Fase 4 — Presentación ejecutiva y entrega final (EFT) (2–3 días)
- T4.1: Preparar presentación (PPT/PDF) orientada a Directorio.
- T4.2: Ensayo de defensa individual y Q&A prep (asignar preguntas por rol).
- T4.3: Empaquetado final: README con pasos para reproducir, requirements, archivos fuente y datasets (o referencias).
- Entregables: Presentación, `EFT_package` en repo.

Tareas transversales
- Documentación continua en `documentation/markdown/`.
- Control de versiones: commits claros y PRs pequeños.
- Backup de imágenes en `images/` y export de datos intermedios en `data/processed/`.

Cronograma orientativo (6 semanas total)
- Semana 1: Fase 0 + Fase 1 (EP1 entregable al final de la semana).
- Semanas 2–3: Fase 2 (EP2 funcional al final de la semana 3).
- Semana 4: Fase 3 (EP3).
- Semana 5: Buffer y optimizaciones.
- Semana 6: Preparación de defensa y entrega final.

Dependencias críticas
- Calidad de datos limpia para construir KPIs financieros.
- Aprobación de prototipos antes de implementar dashboard.

Próximos pasos inmediatos
- Confirmar herramientas para el dashboard.
- Crear templates EP1/EP2 para acelerar entregables.
