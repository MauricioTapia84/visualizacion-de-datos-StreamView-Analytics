---
title: "EP2 — Preparación del dataset para Google Data Studio"
author: "Equipo StreamView (asistente)"
date: 2026-08-31
source_files:
  - src/etl/prepare_data_studio.py
  - data/netflix_movies_detailed_up_to_2025.csv
  - data/netflix_tv_shows_detailed_up_to_2025.csv
---

## Resumen ejecutivo

Para evitar el error de columnas incompatibles en Google Data Studio, se consolidó el catálogo de películas y series en un único esquema compatible. El proceso normaliza nombres, rellena columnas faltantes y crea un archivo único listo para conectar al dashboard. Esta preparación es necesaria antes de construir la visualización final, porque Data Studio exige que todas las fuentes compartan exactamente el mismo esquema.

## 1. Problema técnico identificado

El dataset original presenta una diferencia estructural entre películas y series:

- Películas incluyen `budget` y `revenue`.
- Series no incluyen `budget` ni `revenue`.

Cuando se intenta cargar ambos CSV en la misma fuente o en una unión directa, Data Studio detecta un esquema inconsistente y devuelve un error de columnas no válidas.

## 2. Solución implementada

Se agregó el script:

- `src/etl/prepare_data_studio.py`

Este script expone la función:

```python
consolidate_for_data_studio()
```

y genera el siguiente artefacto:

- `data/processed/catalogo_data_studio.csv`

Además, genera el archivo de metadatos:

- `data/processed/catalogo_data_studio_metadata.json`

## 3. Estructura final del dataset para Data Studio

El dataset consolidado usa este orden de columnas:

```text
show_id, type, title, director, cast, country, date_added, release_year,
rating, duration, genres, language, description, popularity, vote_count,
vote_average, budget, revenue
```

Reglas de consolidación:
- `budget` y `revenue` se mantienen en la misma estructura para ambos tipos.
- Si una fila corresponde a una serie, `budget` y `revenue` quedan en `null`.
- La variable `type` permite diferenciar películas y series en los filtros del dashboard.

## 4. Cómo ejecutar la consolidación

Desde la raíz del repositorio:

```bash
python src/etl/prepare_data_studio.py
```

o, si se está usando el entorno virtual del proyecto:

```bash
.\.venv\Scripts\python.exe src/etl/prepare_data_studio.py
```

## 5. Resultado esperado

Se genera un archivo único en `data/processed/` que está listo para cargar en Google Data Studio sin errores por columnas no coincidentes.

Esto facilita:
- filtros por tipo de contenido
- comparativas por país, género e idioma
- análisis financiero solo para películas
- métricas consistentes para la narrativa del dashboard

## 6. Uso en el dashboard final

El dashboard en Data Studio debe conectarse al CSV consolidado:

- `data/processed/catalogo_data_studio.csv`

De esta forma las visualizaciones quedan alineadas con la estructura que se definió previamente en la documentación EP2.

## 7. Relación con la defensa y el informe ejecutivo

Este proceso debe quedar documentado como parte de la evidencia de preparación del dashboard porque demuestra que:

- se identificó la incompatibilidad técnica de los datasets originales,
- se resolvió con una consolidación reproducible,
- se preservó el contexto de negocio y la capacidad de análisis financiero,
- y se dejó una base estable para la visualización final.

## 8. Recomendación final

No cargar directamente los CSV originales en Data Studio si se pretenden combinar películas y series en una sola visualización. El archivo consolidado debe ser la fuente principal del tablero final.
