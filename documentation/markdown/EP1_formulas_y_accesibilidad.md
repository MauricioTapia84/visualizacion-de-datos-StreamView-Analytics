---
title: "EP1 — Fórmulas, accesibilidad y controles técnicos"
author: "Equipo StreamView"
date: 2026-08-28
source_files:
  - notebooks/EP1_eda_catalogo.ipynb
---

## Fórmulas

- **Popularidad promedio:** media de `popularity` sobre contenidos con valor disponible.
- **Calificación promedio:** media de `vote_average` sobre contenidos con valor disponible.
- **Profit:** `revenue - budget`.
- **ROI aproximado:** `(revenue - budget) / budget`, solo películas con `budget > 0` y `revenue` no nulo.
- **Correlación:** correlación de Pearson entre `budget` y `revenue`; no implica causalidad.
- **Oportunidad proxy:** popularidad normalizada multiplicada por `(1 - participación del catálogo)`.

## Controles ejecutados

No se detectaron valores fuera de rango en años 1900-2025, valoración 0-10, popularidad, votos, presupuesto o ingresos. La cobertura financiera es 4.847/16.000 películas, 30,3%. Se exportan percentiles p01, p25, p50, p75 y p99.

## Accesibilidad

Las visualizaciones usan colores distintos para cada tipo, títulos explícitos, ejes con unidades y escalas logarítmicas rotuladas. En el dashboard se recomienda mantener color y texto, nunca depender solo del color, y comprobar contraste en la revisión visual final.
