---
title: "EP2 — Documentación funcional del dashboard"
author: "Equipo StreamView"
date: 2026-08-28
source_files:
  - dashboard/app.py
  - data/processed/dashboard_visual_plan.csv
---

## Resumen ejecutivo

El dashboard transforma los resultados del EDA en vistas interactivas para Directorio, Contenidos y Marketing.
Usa filtros por tipo y año, compara películas y series, muestra tooltips y permite descargar los datos filtrados.

## Implementación

Ejecutar desde la raíz:

```powershell
python -m pip install -r requirements.txt
streamlit run dashboard/app.py
```

## Vistas

- Popularidad por tipo: ranking separado con valoración y número de votos.
- Géneros: paneles independientes para películas y series.
- Países: paneles independientes para detectar concentración.
- Evolución: línea interactiva por tipo.
- KPIs: contenidos, películas, series y valoración promedio.
- Exportación: descarga CSV del conjunto filtrado.

## Advertencias

`popularity` es un índice relativo. La evolución temporal puede ser plana por la distribución del dataset. Las asociaciones múltiples de países y géneros no deben sumarse como contenidos únicos.
