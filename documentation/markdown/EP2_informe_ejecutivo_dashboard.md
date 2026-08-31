---
title: "EP2 — Informe ejecutivo del dashboard de StreamView Analytics"
author: "Equipo StreamView"
date: 2026-08-31
source_files:
  - data/processed/catalogo_data_studio.csv
  - documentation/markdown/EP2_dashboard_documentation.md
  - documentation/markdown/EP2_dashboard_plan.md
---

## Resumen ejecutivo

El dashboard de StreamView Analytics está orientado a responder tres preguntas clave de negocio: qué estructura tiene el catálogo, qué segmentos tienen mayor potencial y dónde conviene priorizar inversión, contenido y marketing. La solución combina un diagnóstico general del portafolio, análisis geográfico, evaluación de popularidad y revisión del rendimiento financiero de las películas.

A partir del dataset consolidado, se observa que el catálogo está equilibrado entre películas y series, con una fuerte concentración temática en géneros como drama, comedy y animation. Esto sugiere que la oferta actual está orientada a un público amplio y a una estrategia de contenido con gran diversidad temática. Sin embargo, la rentabilidad financiera no siempre acompaña al volumen del contenido, por lo que el dashboard debe servir como herramienta para distinguir entre popularidad, relevancia comercial y retorno real.

## 1. Contexto

El caso semestral plantea construir una solución de visual analytics para StreamView Analytics, centrada en transformar un catálogo audiovisual en información útil para la toma de decisiones. El proyecto ya validó el dataset, lo normalizó y lo preparó para Data Studio con un esquema único compatible para películas y series.

La propuesta final consiste en un dashboard con cuatro vistas:

1. Overview / catálogo general
2. Mercado y catálogo
3. Popularidad y calidad del contenido
4. Financiero

## 2. Objetivo de negocio

El objetivo es apoyar decisiones sobre:

- composición del catálogo
- priorización de segmentos temáticos
- selección de mercados con mayor potencial
- interpretación de la popularidad del contenido
- evaluación de rentabilidad de películas

## 3. Hallazgos clave

### Hallazgo 1 — El portafolio está equilibrado entre películas y series
- El catálogo se divide de forma casi homogénea entre películas y series.
- Esto sugiere que la oferta no está sesgada hacia un único tipo de contenido.
- Relevancia: permite una estrategia balanceada, pero requiere decisiones más precisas para diferenciar contenido y segmentación.

### Hallazgo 2 — Drama, comedy y animation dominan la oferta actual
- Los géneros más presentes son los que más volumen tienen dentro del catálogo.
- Esto indica una estrategia centrada en formatos ampliamente atractivos y de fácil comprensión para público general.
- Relevancia: los mercados y campañas pueden orientarse en función de estos géneros con mayor masa crítica.

### Hallazgo 3 — La popularidad no siempre equivale a rentabilidad
- El dashboard permite distinguir entre contenidos con alta demanda y contenidos con mejor retorno financiero.
- Esto es crítico para la gerencia de contenidos, ya que la popularidad ayuda a decidir qué contenido captar o promocionar, pero no reemplaza la evaluación económica.
- Relevancia: la inversión debe validarse con rentabilidad real, no solo con volumen o engagement relativo.

### Hallazgo 4 — El mercado y la geografía son factores clave para la estrategia
- La organización puede entender no solo qué contenido existe, sino dónde tiene mayor peso y potencial.
- Esto ayuda a crear estrategias de localización, segmentación y promoción orientadas por país, idioma y segmento.

## 4. Recomendaciones ejecutivas

1. Priorizar géneros con mayor combinación de volumen y popularidad
- Deben ser eje de inversión en contenido y campañas de marketing.

2. Segmentar por mercado antes de ampliar inversión
- Se recomienda evaluar por país e idioma para detectar oportunidades reales de crecimiento.

3. Diferenciar inversión entre contenido y rentabilidad
- No todo contenido popular es rentable; la evaluación financiera debe acompañar la estrategia.

4. Usar el dashboard como herramienta de decisión, no solo de observación
- Las visualizaciones deben apoyar decisiones de contenidos, campañas y recursos.

## 5. Qué muestra el dashboard

La vista de overview presenta al usuario la base del análisis: cantidad total, composición, evaluaciones principales y contenidos más relevantes. La segunda vista permite mapear mercados y segmentación por país e idioma. La tercera vista profundiza en popularidad y valoración. La cuarta vista concentra el análisis financiero para aportar rigor y apoyo a decisiones de inversión.

## 6. Relevancia para la rúbrica

El dashboard cumple con la lógica evaluativa de la asignatura porque:

- define una audiencia clara
- responde preguntas de negocio concretas
- usa KPI medibles y explicables
- organiza la narrativa por fases
- presenta recomendaciones basadas en evidencia
- mantiene el proceso reproducible y documentado

## 7. Cierre

El proyecto ya no se ve como una simple exploración de datos, sino como una solución analítica con intención estratégica. La base se ha consolidado con un dataset compatible para Data Studio y una estructura de dashboard que guía al usuario desde el contexto general hacia la recomendación final.

El siguiente paso sería cerrar la implementación visual con Data Studio, validar la legibilidad de cada vista y preparar la defensa final con un enfoque ejecutivo y técnico.
