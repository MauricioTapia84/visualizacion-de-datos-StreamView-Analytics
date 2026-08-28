---
title: "Resumen del Caso Semestral: StreamView Analytics"
author: "Equipo StreamView (asistente)"
date: 2026-08-27
source_files:
  - documentation/markdown/caso_semestral_resumen.md
---

Resumen ejecutivo

El caso semestral plantea diseñar e implementar una solución de Visual Analytics para StreamView Analytics con el objetivo de transformar el catálogo audiovisual en información útil para la toma de decisiones estratégicas. Se proporcionan dos datasets (películas y series, ~16k registros cada uno) y se exige una solución que combine dashboards interactivos, narrativas visuales y documentación reproducible.

Contexto y objetivo

- Empresa: StreamView Analytics — plataforma de streaming en Latinoamérica.
- Objetivo general: crear dashboards, storytelling y productos visuales que apoyen decisiones sobre adquisición, marketing y producto.
- Alcance: análisis y visualizaciones con los datos entregados; no incluye ETL complejo ni modelos predictivos.

Datos y artefactos disponibles

- Datasets: `Netflix Movies Detailed up to 2025` y `Netflix TV Shows Detailed up to 2025`.
- Variables clave: `show_id`, `type`, `title`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `duration`, `genres`, `language`, `description`, `popularity`, `vote_average`, `vote_count`, `budget` (películas), `revenue` (películas).

KPIs y preguntas de negocio

- KPIs de catálogo: total contenidos, películas, series, países, idiomas, géneros.
- KPIs de popularidad/valoración: popularidad promedio, top contenidos, popularidad por género/país, calificación promedio.
- KPIs financieros (películas): presupuesto promedio, ingresos totales, ROI aproximado.
- Preguntas: ¿qué géneros predominan? ¿qué contenidos son más populares? ¿relación presupuesto-revenue? ¿qué mercados priorizar?

Restricciones y reglas de negocio

- `budget` y `revenue` solo para películas.
- `popularity` es índice relativo (no reproducciones).
- Excluir contenidos sin info financiera de KPIs financieros.
- Documentar periodo y alcance de cada análisis.

Entregables por etapa

- EP1: Informe ejecutivo + storytelling (comprensión del negocio y exploración visual).
- EP2: Dashboard interactivo (diseño e implementación).
- EP3: Informe de evaluación crítica y optimización.
- EFT (final): Solución integral + defensa.

Recomendaciones inmediatas

- Priorizar la calidad de datos (nulos, duplicados, formatos de fecha) y documentar transformaciones.
- Definir KPIs mínimos para EP1 y EP2 (lista corta con fórmulas explícitas).
- Estructurar carpetas reproducibles: `data/`, `notebooks/`, `src/`, `dashboard/`, `documentation/markdown/`, `images/`.
