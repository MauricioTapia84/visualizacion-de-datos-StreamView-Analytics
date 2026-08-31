---
title: "EP1 — Data cleaning inicial"
author: "Equipo StreamView (notebook)"
date: 2026-08-28
source_files:
  - c:\Users\shein\OneDrive\Documentos\GitHub\visualizacion-de-datos-StreamView-Analytics\data\netflix_movies_detailed_up_to_2025.csv
  - c:\Users\shein\OneDrive\Documentos\GitHub\visualizacion-de-datos-StreamView-Analytics\data\netflix_tv_shows_detailed_up_to_2025.csv
---

# Resumen de la limpieza inicial

Fecha de ejecución (UTC): 2026-08-28T19:42:09.027233+00:00Z

## Archivo: movies

- Ruta original: c:\Users\shein\OneDrive\Documentos\GitHub\visualizacion-de-datos-StreamView-Analytics\data\netflix_movies_detailed_up_to_2025.csv
- Filas originales: 16000
- Filas después de eliminar duplicados: 16000
- Duplicados (filas completas): 0
- Duplicados por `show_id`: 0
- `date_added` nulos antes: 0
- `date_added` nulos después de parseo: 0
- Filas procesadas guardadas en: c:\Users\shein\OneDrive\Documentos\GitHub\visualizacion-de-datos-StreamView-Analytics\data\processed\movies_processed.csv
- Total de valores nulos (suma por columnas): 17041

### Top 10 columnas por valores faltantes

| Columna | Nulos |
|---|---:|
| duration | 16000 |
| country | 466 |
| cast | 204 |
| director | 132 |
| description | 132 |
| genres | 107 |
| type | 0 |
| show_id | 0 |
| title | 0 |
| date_added | 0 |

## Archivo: tv

- Ruta original: c:\Users\shein\OneDrive\Documentos\GitHub\visualizacion-de-datos-StreamView-Analytics\data\netflix_tv_shows_detailed_up_to_2025.csv
- Filas originales: 16000
- Filas después de eliminar duplicados: 16000
- Duplicados (filas completas): 0
- Duplicados por `show_id`: 9
- `date_added` nulos antes: 0
- `date_added` nulos después de parseo: 0
- Filas procesadas guardadas en: c:\Users\shein\OneDrive\Documentos\GitHub\visualizacion-de-datos-StreamView-Analytics\data\processed\tv_processed.csv
- Total de valores nulos (suma por columnas): 18101

### Top 10 columnas por valores faltantes

| Columna | Nulos |
|---|---:|
| director | 10965 |
| description | 3208 |
| country | 1797 |
| cast | 1157 |
| genres | 974 |
| type | 0 |
| title | 0 |
| show_id | 0 |
| release_year | 0 |
| date_added | 0 |

