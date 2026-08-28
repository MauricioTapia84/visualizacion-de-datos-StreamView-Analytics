---
title: "EP1 — Informe Ejecutivo: Análisis inicial del catálogo"
author: "Equipo StreamView"
date: 2026-08-28
source_files:
  - data/netflix_movies_detailed_up_to_2025.csv
  - data/netflix_tv_shows_detailed_up_to_2025.csv
---

## Resumen ejecutivo

Objetivo: Entregar una visión ejecutiva del catálogo para apoyar decisiones de adquisición y marketing. Este primer entregable sintetiza los hallazgos exploratorios iniciales y propone 3 acciones prioritarias.

Principales hallazgos (borrador)

- Hallazgo A — Composición del catálogo: las series representan una parte significativa del catálogo en número y crecen en diversidad de idiomas.
- Hallazgo B — Géneros dominantes: los géneros X, Y y Z aparecen con mayor frecuencia (detallar tras cálculo).
- Hallazgo C — Popularidad y concentración: un pequeño porcentaje de títulos concentra la mayoría de la popularidad medida por el índice `popularity`.

Recomendación ejecutiva (borrador)

Priorizar adquisiciones en géneros con alta popularidad relativa y mercados donde la proporción de contenido local es baja pero la demanda potencial es alta.

## Metodología

- Limpieza mínima: unificación de formatos de fecha, normalización de países y separación de múltiples géneros por título (registro derivado).
- Alcance: todos los registros disponibles en los dos CSV proporcionados; análisis financiero limitado a registros con `budget` y `revenue` no nulos (películas).

## KPIs calculables (a completar con números)

- Total de contenidos: 
- Nº de películas / Nº de series: 
- Top 10 títulos por `popularity` (lista):
- Popularidad promedio por género (tabla):
- Presupuesto promedio y revenue total (películas con datos):

## Visualizaciones propuestas (incluir en EP1)

- Distribución por tipo (pastel/barras).
- Barras: Top 10 títulos por `popularity`.
- Treemap por género y país.
- Series temporales: `date_added` vs. número de contenidos añadidos por año.

## Próximos pasos inmediatos

1. Ejecutar EDA automático y calcular KPIs básicos (comando sugerido en Python).
2. Insertar cifras reales en este informe y generar figuras.
3. Preparar `EP1_informe_ejecutivo.pdf` y `EP1_informe_ejecutivo_short.pdf` (resumen para Directorio).

## Comandos sugeridos (rápido) para EDA en Python

```python
# crear un entorno virtual
python -m venv .venv
.venv\Scripts\activate
pip install pandas numpy matplotlib seaborn plotly

# ejemplo rápido para conteos
import pandas as pd
movies = pd.read_csv('data/netflix_movies_detailed_up_to_2025.csv')
tv = pd.read_csv('data/netflix_tv_shows_detailed_up_to_2025.csv')
print('Movies:', len(movies))
print('TV shows:', len(tv))
```

