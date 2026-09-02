
# StreamView Analytics

Proyecto académico desarrollado para la asignatura Visualización de Datos.

## Objetivo

Construir una solución de Visual Analytics que permita analizar el
catálogo audiovisual de StreamView Analytics y comunicar información
relevante para la toma de decisiones.

## Estructura

data/raw/
Datos originales proporcionados para el proyecto.

data/processed/
Datos preparados para análisis y visualización.

notebooks/
Procesamiento y preparación de datos.

src/
Scripts reutilizables cuando sean necesarios.

dashboard/
Documentación y recursos relacionados con Looker Studio.

images/
Visualizaciones e imágenes exportadas.

## Preparación de datos

La primera etapa utiliza:

- netflix_movies_detailed_up_to_2025.csv
- netflix_tv_shows_detailed_up_to_2025.csv

El procesamiento se encuentra en:

notebooks/01_limpieza_union.ipynb

El resultado integrado se genera en:

data/processed/catalogo_streamview.csv

## Flujo del proyecto

Datos originales
→ limpieza
→ integración
→ dataset procesado
→ Looker Studio
→ visualizaciones y dashboard

## Herramientas

- Python
- Pandas
- Jupyter / VS Code
- Looker Studio
