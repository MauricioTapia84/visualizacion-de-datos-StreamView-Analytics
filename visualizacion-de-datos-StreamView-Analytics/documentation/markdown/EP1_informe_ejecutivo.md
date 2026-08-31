---
title: "EP1 — Informe Ejecutivo: Análisis inicial del catálogo"
author: "Equipo StreamView"
date: 2026-08-28
source_files:
  - data/netflix_movies_detailed_up_to_2025.csv
  - data/netflix_tv_shows_detailed_up_to_2025.csv
---

## Resumen ejecutivo

Objetivo: entregar una visión ejecutiva del catálogo para apoyar decisiones de adquisición y marketing. El EDA analiza 32.000 contenidos incorporados entre 2010 y 2025.

Principales hallazgos

- Hallazgo A — Drama lidera las asociaciones temáticas con 14.688 contenidos, seguido por Comedy y Animation.
- Hallazgo B — The Late Show with Stephen Colbert lidera el índice de popularidad con 6.421,92; el índice no representa reproducciones.
- Hallazgo C — En 4.847 películas con datos financieros válidos, la correlación budget-revenue es 0,730, pero el ROI mediano es -22,2%.

Recomendaciones ejecutivas

1. Priorizar análisis de adquisición en géneros con alta popularidad relativa y baja saturación, diferenciando películas y series.
2. Usar Brasil, Colombia, Chile y México como hipótesis de investigación, validando demanda, costos y competencia antes de invertir.
3. Evaluar títulos financieros individualmente: el presupuesto se relaciona con ingresos, pero no garantiza rentabilidad.

## Metodología

- Limpieza inicial reproducible en [EP1_initial_cleaning_colab.ipynb](../../notebooks/EP1_initial_cleaning_colab.ipynb).
- EDA independiente en [EP1_eda_catalogo.ipynb](../../notebooks/EP1_eda_catalogo.ipynb), con separación de géneros, países e idiomas sin duplicar KPIs de contenidos.
- Alcance: 16.000 películas y 16.000 series. Las finanzas incluyen únicamente películas con `budget` y `revenue` válidos y `budget > 0`.

## KPIs calculados

- Total de contenidos: 32.000.
- Películas / series: 16.000 / 16.000.
- Países / idiomas / géneros: 147 / 83 / 28.
- Popularidad promedio / calificación promedio: 42,62 / 5,69.
- Presupuesto promedio: 28.939.280; ingresos totales: 367.371.400.000.
- Cobertura financiera: 4.847 de 16.000 películas, 30,3%.
- Tablas detalladas: `data/processed/`.

## Visualizaciones seleccionadas

- Ranking de popularidad separado entre películas y series.
- Géneros y países comparados en paneles independientes por tipo.
- Evolución anual en paneles separados por tipo.
- Dispersión presupuesto-ingresos con escala logarítmica.
- No se incluye una gráfica de composición independiente: la información se presenta como KPI.

Las figuras están en `images/` y la matriz de uso para el dashboard en `data/processed/dashboard_visual_plan.csv`.

## Limitaciones

- `popularity` es un índice relativo, no una métrica de reproducciones.
- La serie temporal es plana porque el dataset contiene 1.000 películas y 1.000 series por año.
- Los países y géneros son asociaciones; un título puede aparecer en más de una categoría.
- El proxy de mercados no sustituye una investigación de demanda.

## Próximos pasos

1. Ejecutar `streamlit run dashboard/app.py` y revisar el dashboard.
2. Realizar la prueba de usabilidad definida en [EP3_usabilidad_evaluacion.md](EP3_usabilidad_evaluacion.md).
3. Exportar este informe a PDF y preparar la presentación ejecutiva.

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

