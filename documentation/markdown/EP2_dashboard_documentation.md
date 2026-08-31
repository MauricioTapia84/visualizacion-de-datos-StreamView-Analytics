---
title: "EP2 — Documentación técnica del dashboard en Data Studio"
author: "Equipo StreamView"
date: 2026-08-31
source_files:
  - data/processed/catalogo_data_studio.csv
  - src/etl/prepare_data_studio.py
  - documentation/markdown/EP2_dashboard_plan.md
---

## Resumen ejecutivo

Este documento describe la estructura del dashboard final que se construirá en Google Data Studio para StreamView Analytics. La propuesta sigue la lógica de la rúbrica y del caso semestral: cada vista responde a una pregunta de negocio, usa KPI ejecutivos y permite que la audiencia tome decisiones operativas o estratégicas con base en evidencia.

El dashboard está diseñado para tres públicos principales: dirección ejecutiva, gerencia de contenidos y marketing. La narrativa empieza con un panorama general del catálogo, luego avanza hacia mercado, popularidad y financiera, para cerrar con recomendaciones accionables.

## 1. Objetivo del dashboard

El dashboard tiene como propósito apoyar decisiones sobre:

- composición del portafolio de contenidos
- priorización de géneros y mercados
- evaluación de popularidad por contenido y tipo
- análisis de la rentabilidad financiera de películas
- propuesta de recomendaciones estratégicas para inversión y crecimiento

La clave es que no sea solo una colección de gráficos, sino una herramienta de análisis y decisión para la organización.

## 2. Audiencia y decisiones que apoya

### 2.1 Dirección ejecutiva
- ¿Qué estructura tiene el catálogo?
- ¿Qué segmentos tienen más potencial?
- ¿Dónde conviene invertir o expandirse?

### 2.2 Gerencia de contenidos
- ¿Qué tipos de contenido dominan y qué funciona mejor?
- ¿Qué géneros y países merecen más atención?
- ¿Qué títulos o mercados son más relevantes?

### 2.3 Marketing / crecimiento
- ¿En qué mercados conviene enfocar campañas?
- ¿Qué perfiles de contenido tienen mayor atractivo por región?
- ¿Qué patrones de contenido pueden apoyar estrategias de promoción?

## 3. Fuente de datos

El dashboard se alimenta del archivo consolidado preparado para Data Studio:

- `data/processed/catalogo_data_studio.csv`

Dicho dataset se genera con:

- `src/etl/prepare_data_studio.py`

Este archivo unifica películas y series en un mismo esquema, manteniendo columnas financieras para las películas y dejando `budget` / `revenue` nulos para series. Ese proceso evita el problema de columnas incompatibles que ocurre al cargar ambos CSV originales en Data Studio.

## 4. Reproducibilidad

### Generar el dataset listo para Data Studio

```bash
python src/etl/prepare_data_studio.py
```

### Verificar la salida

- `data/processed/catalogo_data_studio.csv`
- `data/processed/catalogo_data_studio_metadata.json`

## 5. Estructura del dashboard

Se recomienda que el dashboard se organice en 4 vistas, siguiendo un patrón de narrativa ejecutiva:

1. Overview / catálogo general
2. Mercado y catálogo
3. Popularidad y calidad del contenido
4. Financiero

## 6. Layout recomendado por vista

### Vista 1 — Overview
Se recomienda un layout tipo F:

- fila superior: KPI cards
- mitad izquierda: composición del catálogo
- mitad derecha: géneros dominantes
- fila inferior: top títulos por popularidad

Razón:
- permite lectura rápida y jerárquica
- el usuario primero compara KPIs, luego interpreta composición, y finalmente entra al detalle
- se alinea con la necesidad de una vista ejecutiva, clara y de alto impacto

### Vista 2 — Mercado y catálogo
- mapa por país
- barras por idioma
- barras por género
- evolución anual del catálogo

### Vista 3 — Popularidad y calidad
- top 10 títulos
- popularidad promedio por género
- rating o score por género
- comparación de popularidad por año

### Vista 4 — Financiero
- KPI financiero de presupuesto y retorno
- scatter de budget vs revenue
- ROI por género o mercado
- tabla de películas con mayor rentabilidad

## 7. KPI definidos para el dashboard

### 7.1 KPIs de catálogo

- Total de contenidos: `count(title)`
- Películas: `count(type = 'Movie')`
- Series: `count(type = 'TV Show')`
- Países representados: `nunique(country)`
- Idiomas representados: `nunique(language)`
- Géneros principales: `count(genres)`

### 7.2 KPIs de popularidad

- Popularidad promedio: `mean(popularity)`
- Rating promedio: `mean(vote_average)`
- Top títulos por popularidad: orden descendente por `popularity`
- Popularidad por género: `mean(popularity) grouped by genre`

### 7.3 KPIs financieros

- Presupuesto promedio: `mean(budget)`
- Ingresos totales: `sum(revenue)`
- ROI aproximado: `((revenue - budget) / budget) * 100`
- Correlación presupuesto-ingresos: `corr(budget, revenue)`

## 8. Filtros que debe incluir el dashboard

- type
- country
- genre
- release_year
- language
- rating
- popularity

Estos filtros permiten hacer comparativas útiles sin saturar la visualización y ayudan a la exploración analítica de la audiencia.

## 9. Recomendaciones de diseño para Data Studio

- Priorizar KPI cards en la parte superior para una lectura ejecutiva.
- Diferenciar películas y series con colores muy claros y consistentes.
- Usar texto claro en cada bloque: título, subtítulo, unidad y contexto.
- Mantener la jerarquía visual: primero la narrativa general, luego la comparación, luego el detalle.
- Añadir un insight clave de texto en cada vista para facilitar la defensa.
- Usar tablas solo como complemento a los gráficos principales.

## 10. Guion visual de cada página

### Vista 1 — Overview
Pregunta: ¿Cuál es la composición y volumen del catálogo?

Respuesta visual:
- KPI cards muestran el tamaño del catálogo y la proporción de tipos
- donut indica balance películas/series
- barras de géneros miden la concentración del catálogo
- ranking muestra títulos más relevantes

### Vista 2 — Mercado y catálogo
Pregunta: ¿Dónde está el mercado y qué segmentos tienen más potencial?

Respuesta visual:
- mapa por país da contexto geográfico
- barras por idioma muestra diversidad regional
- barras por género revelan especialización del contenido
- línea por año indica evolución del catálogo

### Vista 3 — Popularidad
Pregunta: ¿Qué contenidos y géneros funcionan mejor?

Respuesta visual:
- ranking de popularidad identifica contenidos líderes
- barras de popularidad por género detectan fortalezas temáticas
- scatter de rating vs popularidad compara demanda y valoración

### Vista 4 — Financiero
Pregunta: ¿La estrategia financiera es sostenible?

Respuesta visual:
- KPI financiero resume inversión y retorno
- scatter budget vs revenue muestra correlación
- ROI por género guía decisiones de inversión
- tabla final permite priorizar títulos con mejor potencial

## 11. Consideraciones de negocio

- `popularity` es un índice relativo y no representa reproducciones reales.
- `budget` y `revenue` solo deben usarse en el segmento de películas.
- `duration` para películas requiere cuidado antes de usarla como KPI a gran escala, porque no estaba completamente poblada en el dataset raw.
- El dashboard debe usar evidencia clara y no solo comparativas visuales; cada decisión debe poder justificarse.

## 12. Cierre

La versión final del dashboard debe verse como una narrativa de negocio con estructura ejecutiva: primero contexto, luego análisis, luego decisiones. La visión general del catálogo, la segmentación geográfica y la evaluación de popularidad y rentabilidad forman la base para una defensa sólida y una recomendación accionable.
