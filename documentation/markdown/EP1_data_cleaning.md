---
title: "EP1 — Data cleaning inicial (documentación)"
author: "Equipo StreamView (asistente)"
date: 2026-08-28
source_files:
  - src/etl/initial_cleaning.py
  - data/netflix_movies_detailed_up_to_2025.csv
  - data/netflix_tv_shows_detailed_up_to_2025.csv
---

## Objetivo

Este documento describe el proceso automático de extracción y limpieza inicial implementado en `src/etl/initial_cleaning.py`. El script elimina duplicados, normaliza cadenas, parsea la columna `date_added` y genera archivos procesados en `data/processed/`.

## Pasos realizados por el script

- Lectura de los CSV originales en `data/`.
- Conteo de filas originales y detección de duplicados (filas completas y por `show_id` cuando existe).
- Eliminación de duplicados completos.
- Normalización de valores de texto (trim) y conversión de valores vacíos a `NA`.
- Parseo de `date_added` a tipo fecha (si existe la columna).
- Homogeneización de la columna `country` (capitalización simple).
- Recuento de valores nulos por columna y listado top 10.
- Salida: archivos `data/processed/movies_processed.csv` y `data/processed/tv_processed.csv`.

## Cómo ejecutar (entorno local)

A continuación los comandos sugeridos para ejecutar el script en tu equipo Windows (desde la raíz del repo):

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install pandas
python src/etl/initial_cleaning.py
```

Si tu `python` apunta al Microsoft Store o no está instalado, instala Python 3.8+ desde https://www.python.org/downloads/ antes de ejecutar los comandos.

## Resultados esperados

Al ejecutar el script se crearán:

- `data/processed/movies_processed.csv`
- `data/processed/tv_processed.csv`
- (si el script se ejecuta) este mismo archivo debería actualizarse con los recuentos reales de filas, duplicados y nulos por columna.

## Estado actual

- El script `src/etl/initial_cleaning.py` fue creado en el repositorio.
- No se pudo ejecutar el script desde este entorno porque `python` y `pip` no están disponibles aquí. Por tanto, los CSV procesados y los recuentos reales aún no se han generado.

## Próximos pasos recomendados

1. Ejecutar los comandos anteriores en tu entorno local para generar los archivos procesados y actualizar este informe con los resultados reales.
2. Revisar las columnas con mayor cantidad de nulos y decidir: imputar, eliminar o documentar limitaciones.
3. Añadir transformaciones adicionales (p.ej. separación de múltiples géneros) según necesidades del análisis.

Si quieres, puedo ajustar el script para:

- Guardar un CSV con los registros descartados por duplicado en `data/processed/discarded_duplicates.csv`.
- Exportar un JSON con estadísticas más detalladas por columna.

Indícame qué quieres que agregue y lo incorporo.
