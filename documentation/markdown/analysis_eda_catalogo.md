---
title: 'EDA completo - StreamView Analytics'
author: 'Equipo StreamView - Data Analyst / Visual Designer'
date: 2026-08-28
source_files:
  - notebooks/EP1_eda_catalogo.ipynb
  - data/processed/movies_processed.csv
  - data/processed/tv_processed.csv
---

## Resumen ejecutivo

El catálogo contiene 32,000 contenidos, con 16,000 películas y 16,000 series. Drama es el género dominante. La correlación presupuesto-ingresos es 0.730, mientras el ROI mediano es -22.2%.

## Preguntas del caso

- **Géneros predominantes:** Drama, seguido por Comedy y Animation.
- **Contenidos más populares:** The Late Show with Stephen Colbert, con índice 6421.92; no equivale a reproducciones.
- **Relación budget-revenue:** positiva en 4,847 películas válidas, pero no causal.
- **Mercados prioritarios:** el proxy identifica Portugal; entre los mercados latinoamericanos aparecen Brazil, Colombia, Chile, Mexico.
- **KPIs:** se exportan en data/processed/ junto con países, idiomas, géneros, popularidad, evolución y finanzas.

## Plan para el dashboard

La matriz completa se encuentra en `data/processed/dashboard_visual_plan.csv`. Se priorizan rankings de popularidad separados por tipo, géneros y países comparados entre películas y series, una línea temporal en paneles independientes y una dispersión financiera logarítmica. La composición general queda como KPI, no como gráfico independiente.

La serie temporal es plana porque el dataset contiene exactamente 1.000 películas y 1.000 series incorporadas en cada año entre 2010 y 2025. Debe interpretarse como una limitación de los datos.

## Reproducibilidad

Ejecutar primero `notebooks/EP1_initial_cleaning_colab.ipynb` y después este notebook. Se generan 9 tablas, 5 figuras vigentes en `images/` y una matriz de planificación para construir el dashboard.
