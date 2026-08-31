---
title: "EP2 — Validación del dataset para Data Studio"
author: "Equipo StreamView (asistente)"
date: 2026-08-31
source_files:
  - data/netflix_movies_detailed_up_to_2025.csv
  - data/netflix_tv_shows_detailed_up_to_2025.csv
  - src/etl/initial_cleaning.py
---

## Resumen ejecutivo

Se validó el dataset base para la construcción del dashboard en Data Studio. El estado general es bueno para continuar: no hay filas duplicadas, la estructura principal es consistente entre ambos tipos de contenido y los campos clave para KPI están identificados. La única diferencia esperada es que las películas incluyen columnas financieras (`budget`, `revenue`), mientras que las series no las tienen.

## 1. Verificación de integridad del dataset

### 1.1 Duplicados
- Películas: 0 filas duplicadas.
- Series: 0 filas duplicadas.

### 1.2 Volumen de registros
- Películas: 16.000 filas.
- Series: 16.000 filas.

### 1.3 Registro de nulos relevantes

Películas:
- `duration`: 16.000 nulos (todas las filas sin valor usable)
- `country`: 466 nulos
- `cast`: 204 nulos
- `director`: 132 nulos
- `description`: 132 nulos
- `genres`: 107 nulos

Series:
- `director`: 10.965 nulos
- `description`: 3.206 nulos
- `country`: 1.797 nulos
- `cast`: 1.157 nulos
- `genres`: 974 nulos
- El resto de columnas clave no presenta nulos relevantes.

### 1.4 Estructura esperada de columnas

Películas tienen 18 columnas:
- `show_id`, `type`, `title`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `duration`, `genres`, `language`, `description`, `popularity`, `vote_count`, `vote_average`, `budget`, `revenue`

Series tienen 16 columnas:
- `show_id`, `type`, `title`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `duration`, `genres`, `language`, `description`, `popularity`, `vote_count`, `vote_average`

Conclusión clave:
- La diferencia entre estructuras es esperada.
- `budget` y `revenue` aparecen solo en películas, porque son atributos financieros no presentes en series.
- `duration` para películas está totalmente vacío en el raw dataset, por lo que no debe usarse como KPI directo sin una normalización adicional o una decisión de negocio explícita.

## 2. Registro de limpieza aplicada y decisiones de normalización

Basado en el pipeline de `src/etl/initial_cleaning.py`, la limpieza documental incluye:

- eliminación de filas duplicadas completas
- normalización de espacios en columnas tipo texto
- reemplazo de cadenas vacías, `None`, `nan` por valores nulos estandarizados
- parseo de `date_added` a formato de fecha
- limpieza de `country` y normalización de text
- registro de nulos y export de un resumen en `documentation/markdown/`

### 2.1 Valores que se reemplazan o estandarizan
- cadenas vacías -> `NA`
- `None` -> `NA`
- `nan` -> `NA`
- espacios en columnas de texto -> trim
- fechas con formato no consistente -> parseo a fecha válida

### 2.2 Columnas relevantes para el dashboard

Para el proyecto de Data Studio, las columnas relevantes son:

- `type`
- `title`
- `country`
- `date_added`
- `release_year`
- `rating`
- `duration`
- `genres`
- `language`
- `description`
- `popularity`
- `vote_count`
- `vote_average`
- `budget` (solo películas)
- `revenue` (solo películas)

Columnas que requieren cuidado:
- `duration` en películas: no aporta datos útiles en el raw dataset y debe tratarse como campo especial o descartarse para KPIs cuantitativos.
- `director` y `cast`: útiles para análisis complementarios, pero no son el eje principal del dashboard.

## 3. Mapeo de variables por KPI

### 3.1 KPI operativos
- Total de contenidos: `count(title)`
- Películas vs series: `type`
- Países: `country`
- Idiomas: `language`
- Géneros: `genres`

### 3.2 KPI de popularidad
- Popularidad promedio: `popularity`
- Rating promedio: `vote_average` o `rating` según el tipo de uso y la variable final validada
- Top títulos por popularidad: `title` + `popularity`

### 3.3 KPI financieros (solo para películas)
- Presupuesto promedio: `budget`
- Ingresos totales: `revenue`
- ROI aproximado: `((revenue - budget) / budget) * 100`
- Relación presupuesto vs ingresos: `budget` y `revenue`

### 3.4 KPI de segmentación por mercado
- Géneros por país: `genres` + `country`
- Idiomas más relevantes: `language`
- Evolución anual: `release_year` y/o `date_added`

## 4. Estado de cumplimiento de la validación

Se cumple lo solicitado:
- [x] Dejar el dataset validado y documentado como base para Data Studio
- [x] Revisar duplicados, nulos, columnas clave y formatos
- [x] Confirmar que movies y tv tienen la misma estructura esperada
- [x] Dejar registro de qué limpiamos, qué valores reemplazamos y qué columnas quedan relevantes
- [x] Documentar qué variables se usan para cada KPI

## 5. Observación importante para el dashboard

Aunque la estructura global está bien, el proyecto aún necesita decidir dos aspectos antes de pasar a Data Studio:

1. Si `duration` debe descartarse para películas o normalizarse con otra fuente externa.
2. Si la audiencia del dashboard prioriza métricas de negocio (`budget`, `revenue`, ROI) más que métricas de contenido (`duration`, director, cast).

Esto no bloquea el proceso, pero sí define la lógica de diseño del dashboard y de la defensa final.
