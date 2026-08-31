---
title: "EP2 — Guía paso a paso de las vistas del dashboard"
author: "Equipo StreamView"
date: 2026-08-31
source_files:
  - data/processed/catalogo_data_studio.csv
  - documentation/markdown/dashboard_mockup_overview.html
  - documentation/markdown/dashboard_mockup_mercado.html
  - documentation/markdown/dashboard_mockup_popularidad.html
  - documentation/markdown/dashboard_mockup_financiero.html
---

## Resumen ejecutivo

Esta guía explica cómo construir cada una de las vistas del dashboard en Google Data Studio y qué elementos deben incluirse para que cada pantalla responda a preguntas de negocio concretas. Además, incluye mockups HTML para visualizar la propuesta antes de implementarla en la herramienta final.

## 1. Estructura general del dashboard

El dashboard se organiza en 4 vistas:

1. Overview / catálogo general
2. Mercado y catálogo
3. Popularidad y calidad del contenido
4. Financiero

La recomendación de layout es F para la primera vista y una composición de lectura lógica para las siguientes, con filtros globales en la parte superior y KPIs visibles desde el inicio.

## 2. Vista 1 — Overview del catálogo

### Objetivo
Responder: ¿cuánto contenido existe y cómo se distribuye?

### Elementos clave
- KPI cards:
  - Total de contenidos
  - Películas
  - Series
  - Popularidad promedio
- Gráfico 1: donut o barra apilada con composición por tipo
- Gráfico 2: barras horizontales de géneros dominantes
- Tabla: top 10 contenidos por popularidad

### Pasos recomendados en Data Studio

1. Crea una página llamada `Overview`.
2. Agrega filtros globales: `type`, `country`, `genre`, `year`, `language`.
3. Inserta 4 KPI cards en la parte superior.
4. Añade un gráfico circular o de barras apiladas para `type`.
5. Añade un gráfico de barras horizontales para `genre`.
6. Añade una tabla con `title`, `type` y `popularity` ordenada descendente.
7. Escribe un texto breve con el insight principal: “El catálogo está equilibrado entre películas y series, con dominancia de drama, comedy y animation”.

### Mockup visual

- [dashboard_mockup_overview.html](dashboard_mockup_overview.html)

## 3. Vista 2 — Mercado y catálogo

### Objetivo
Responder: ¿en qué mercados y segmentos hay más potencial?

### Elementos clave
- Mapa por país
- Barras por idioma
- Barras por género
- Línea o área por año

### Pasos recomendados en Data Studio

1. Crea una página llamada `Mercado y catálogo`.
2. Mantén los mismos filtros globales.
3. Añade un mapa con dimensión `country` y métrica `count(title)`.
4. Añade un gráfico de barras por `language`.
5. Añade un gráfico de barras por `genre`.
6. Añade una línea temporal con `release_year` y `count(title)`.
7. Añade un pequeño insight: “La expansión del catálogo se concentra en determinados mercados y géneros”.

### Mockup visual

- [dashboard_mockup_mercado.html](dashboard_mockup_mercado.html)

## 4. Vista 3 — Popularidad y calidad del contenido

### Objetivo
Responder: ¿qué contenidos y géneros funcionan mejor?

### Elementos clave
- Top 10 títulos por popularidad
- Barras por popularidad promedio por género
- Scatter o diagrama de dispersión de `vote_average` vs `popularity`
- Evolución anual de la popularidad media

### Pasos recomendados en Data Studio

1. Crea una página llamada `Popularidad`.
2. Usa un ranking con `title`, `type` y `popularity`.
3. Añade un gráfico de barras para `genre` con promedio de `popularity`.
4. Añade un scatter usando `vote_average` y `popularity`.
5. Añade una gráfica de línea por `release_year` para observar tendencia.
6. Añade un insight: “La popularidad no siempre coincide con la valoración por género; conviene revisarlo junto con la demanda y la inversión”.

### Mockup visual

- [dashboard_mockup_popularidad.html](dashboard_mockup_popularidad.html)

## 5. Vista 4 — Financiero

### Objetivo
Responder: ¿la inversión financiera está generando valor?

### Elementos clave
- KPI cards financieros:
  - presupuesto promedio
  - ingresos totales
  - ROI promedio
- Scatter de `budget` vs `revenue`
- Barras de ROI por género
- Tabla con películas de mayor retorno

### Pasos recomendados en Data Studio

1. Crea la página `Financiero`.
2. Aplica un filtro `type = Movie` para enfocarte en el segmento financiero.
3. Añade KPI cards de `budget`, `revenue` y ROI.
4. Usa un scatter con `budget` vs `revenue`.
5. Calcula ROI con la expresión:

```text
((revenue - budget) / budget) * 100
```

6. Añade barras por `genre` con valor de ROI promedio.
7. Añade una tabla con top películas por retorno.
8. Añade un insight: “El retorno financiero no es homogéneo; debe evaluarse por género y por película”.

### Mockup visual

- [dashboard_mockup_financiero.html](dashboard_mockup_financiero.html)

## 6. Recomendación de orden de implementación

1. Completar la vista 1 Overview
2. Construir la vista 2 Mercado
3. Construir la vista 3 Popularidad
4. Construir la vista 4 Financiero

Esto mantiene una narrativa lógica y facilita la validación de la defensa final.

## 7. Cierre

Cada vista debe responder una pregunta concreta y cada gráfico debe estar alineado con una decisión de negocio. El mockup HTML sirve como guía de composición visual antes de replicar la página en Data Studio.
