# Fuentes finales para Looker Studio

Estas fuentes se generan ejecutando `python3 src/pipeline/fuentes_dashboard_finales.py` desde la raíz del proyecto. El pipeline parte directamente de los CSV oficiales en `data/raw/` y no modifica los archivos originales.

## dashboard_contenidos_final.csv

- Granularidad: una fila por contenido (32000 filas).
- Uso: fuente principal de Looker Studio.
- El identificador `id_contenido` se construye desde `type` y `show_id`; las colisiones dentro del mismo tipo se resuelven con un hash determinista de la fila original.
- No contiene índices ni predicciones del modelado experimental.

## dashboard_generos.csv

- Granularidad: una fila por relación contenido-género (65900 filas).
- Uso: ranking, comparación y análisis correcto de géneros.
- Los géneros se separan por coma, se recortan espacios y se preservan las categorías originales sin fusionarlas.

## dashboard_paises.csv

- Granularidad: una fila por relación contenido-país (37636 filas).
- Uso: mapa y análisis geográfico.
- Los países se separan por coma, se recortan espacios y se mantienen los nombres originales.

## Origen y tratamiento

- Movies: `data/raw/netflix_movies_detailed_up_to_2025.csv`.
- TV Shows: `data/raw/netflix_tv_shows_detailed_up_to_2025.csv`.
- La integración es vertical; no se realiza JOIN entre Movies y TV Shows.
- `budget` y `revenue` se conservan únicamente para Movies.
- Los ceros financieros se interpretan como ausencia y se exportan como campos vacíos/NULL.
- No se imputan datos financieros ni se convierten NULL a cero.
- Las relaciones repetidas `id_contenido + categoría` se eliminan de las tablas normalizadas.

## Validación

El detalle reproducible está en `dashboard_validation.json` y `dashboard_validation.md`.

El modelado predictivo existente no se elimina, pero permanece separado en `data/processed/predictive/`. Sus predicciones actuales se generan sobre las 32.000 filas y mezclan observaciones de entrenamiento y prueba; además, `indice_exito` usa variables que también recibe el modelo.
