---
title: "EP2 — Definición de audiencia, KPIs, narrativa y wireframe del dashboard"
author: "Equipo StreamView (asistente)"
date: 2026-08-31
source_files:
  - data/netflix_movies_detailed_up_to_2025.csv
  - data/netflix_tv_shows_detailed_up_to_2025.csv
  - src/etl/initial_cleaning.py
  - documentation/markdown/caso_semestral_resumen.md
  - documentation/markdown/rubrica_pautas_resumen.md
---

## Resumen ejecutivo

Antes de construir el dashboard en Data Studio, hay que dejar definidos el público, los KPIs, la narrativa y la estructura de la interfaz. Esta base permite que el tablero responda a decisiones reales de negocio y no solo a visualizaciones decorativas. El objetivo es preparar un conjunto de métricas y pantallas que sustenten la estrategia del catálogo de Netflix en StreamView Analytics.

## 1. Audiencia objetivo

### 1.1 Audiencia principal del proyecto
La audiencia principal es la dirección ejecutiva y la gerencia de contenidos, porque la decisión más relevante del dashboard es orientar la estrategia del catálogo y la inversión en contenido.

- Objetivo principal: decidir qué tipos de contenidos priorizar y en qué mercados crecer.
- Audiencia secundaria: marketing y expansión de negocio.
- Uso esperado: análisis estratégico para apoyar decisiones de adquisición, segmentación de mercado y combinación de géneros.

### 1.2 Preguntas clave de negocio para la audiencia principal
- ¿Qué composición tiene el catálogo actual y en qué proporción están películas y series?
- ¿Qué géneros son más relevantes en volumen y popularidad?
- ¿Qué mercados y países concentran mayor potencial?
- ¿Qué contenidos generan mejor popularidad relativa?
- ¿Existe una relación clara entre presupuesto e ingresos para las películas?
- ¿Qué segmentos del catálogo deberían priorizarse para inversión o expansión?

### 1.3 KPI prioritarios por usuario
- Dirección ejecutiva:
  - volumen total de contenidos
  - proporción películas/series
  - popularidad promedio
  - países y géneros más relevantes
  - ROI promedio de películas
- Gerencia de contenidos:
  - top géneros por popularidad
  - top títulos por popularidad
  - contenido por país/idioma
  - rentabilidad por categoría
- Marketing / crecimiento:
  - contenido destacado por mercado
  - composición por país y género
  - tendencia anual por tipo de contenido

## 2. Propósito del dashboard

El dashboard debe servir como herramienta de decisión para evaluar el catálogo desde tres ángulos: composición, valor y oportunidades de negocio. No debe exhibirse como un tablero de “datos curiosos”, sino como un panel que responda preguntas de inversión, contenido y estrategia de mercado. La historia debe ir de contexto global a decisiones accionables.

## 3. KPI mínimo que debe incluir el dashboard

### 3.1 KPIs operativos
- Total de contenidos
  - Definición: número total de registros del catálogo.
  - Fórmula: count(title)
- Distribución por tipo
  - Definición: proporción de películas y series.
  - Fórmula: count(type) por categoría
- Países y idiomas representados
  - Definición: número de países e idiomas con presencia en el catálogo.
  - Fórmula: distinct(country), distinct(language)
- Géneros principales
  - Definición: conteo de géneros más frecuentes.
  - Fórmula: count(genre) por categoría

### 3.2 KPIs de popularidad y valoración
- Popularidad promedio
  - Definición: nivel medio de popularidad del catálogo.
  - Fórmula: mean(popularity)
- Rating promedio
  - Definición: promedio general de la valoración del público.
  - Fórmula: mean(vote_average) o rating medio disponible
- Top 10 de contenidos más populares
  - Definición: lista de títulos con mayor popularidad relativa.
  - Fórmula: sort by popularity desc
- Top géneros por popularidad
  - Definición: géneros con mejor combinación de volumen y relevancia.
  - Fórmula: mean popularity por genre

### 3.3 KPIs financieros (solo películas)
- Presupuesto promedio
  - Fórmula: mean(budget)
- Ingresos totales
  - Fórmula: sum(revenue)
- ROI aproximado
  - Fórmula: ((revenue - budget) / budget) * 100
- Relación presupuesto-ingresos
  - Definición: comparación entre inversión y retorno por película.
  - Fórmula: scatter plot o correlación

### 3.4 KPIs estratégicos de mercado
- Géneros por país
- Idiomas más relevantes por región
- Distribución de contenidos por año
- Evolución anual de cartera por tipo

## 4. Preguntas de negocio que debe responder el dashboard

1. ¿Qué proporción del catálogo corresponde a películas y series?
2. ¿Qué géneros dominan la oferta actual?
3. ¿Qué países o idiomas concentran mayor volumen de contenido?
4. ¿Qué títulos o géneros presentan mejor popularidad relativa?
5. ¿Qué mercados y categorías tienen más potencial de expansión?
6. ¿La inversión financiera se acompaña de mayor retorno?
7. ¿Hay diferencias relevantes entre películas y series en cuanto a demanda y estructura del catálogo?
8. ¿Dónde conviene priorizar inversión o campañas de adquisición?

## 5. Fórmulas exactas por sección del dashboard

### 5.1 Sección catálogo general
- Total de contenidos: `count(title)`
- Películas: `count(type == 'Movie')`
- Series: `count(type == 'TV Show')`
- Proporción por tipo: `(count(type) / total_contenidos) * 100`
- Países representados: `nunique(country)`
- Idiomas representados: `nunique(language)`
- Géneros principales: `value_counts(genres)`

### 5.2 Sección popularidad
- Popularidad promedio: `mean(popularity)`
- Rating promedio: `mean(vote_average)`
- Top títulos por popularidad: `sort_values(popularity, ascending=False).head(10)`
- Popularidad por género: `mean(popularity) group by genre`

### 5.3 Sección mercado y segmentación
- Contenido por país: `count(title) group by country`
- Contenido por idioma: `count(title) group by language`
- Contenido por año: `count(title) group by release_year`
- Evolución anual por tipo: `count(title) group by type, release_year`

### 5.4 Sección financiera (películas)
- Presupuesto promedio: `mean(budget)`
- Ingresos totales: `sum(revenue)`
- ROI aproximado: `((revenue - budget) / budget) * 100`
- Correlación presupuesto-ingresos: `corr(budget, revenue)`

## 6. Dataset limpio y documentado antes de Data Studio

Antes de conectar Data Studio, el dataset debe quedar validado y documentado para evitar errores de interpretación en el dashboard.

### 5.1 Tareas de limpieza mínimas
- Eliminar duplicados completos y duplicados por `show_id` cuando aplique.
- Normalizar espacios en textos y columnas object.
- Corregir formatos de fecha en `date_added`.
- Estandarizar valores de `country`, `genre`, `language` y similares.
- Reemplazar cadenas vacías y valores anómalos por `NA`/nulo.
- Revisar nulos por columna y dejar registro de impacto.
- Separar datos financieros para películas y dejar claro qué columnas no aplican a series.

### 5.2 Estado recomendado del dataset
- Archivo procesado: `data/processed/movies_processed.csv`
- Archivo procesado: `data/processed/tv_processed.csv`
- Registro de calidad: generado por el script ETL.
- Documentación de nulls y transformaciones: en `documentation/markdown/`.

### 5.3 Reproducción del pipeline

Comando principal:

```bash
python src/etl/initial_cleaning.py
```

Esto debe dejar listo el dataset de entrada para cualquier tablero posterior, incluyendo el export de metadatos y reportes del proceso de limpieza.

## 7. Narrativa de negocio del dashboard

La historia visual debe guiar al usuario desde la composición general hacia decisiones estratégicas concretas.

### Sección 1 — Estado general del catálogo
- Mostrar composición global del catálogo.
- Responder: ¿cuántos contenidos hay y cómo se distribuyen?
- Decisión de negocio apoyada: detectar si el portafolio está equilibrado o sesgado.

### Sección 2 — Qué está funcionando mejor
- Mostrar top géneros, países y títulos según popularidad.
- Responder: ¿qué segmentos tienen mejor respuesta?
- Decisión de negocio apoyada: orientar inversión en contenido, campañas y adquisición.

### Sección 3 — Dónde hay oportunidad de crecimiento
- Comparar por región, idioma y género.
- Responder: ¿qué mercados y segmentos están subexplotados o interesantes?
- Decisión de negocio apoyada: priorizar expansión geográfica y segmentación de contenido.

### Sección 4 — Rendimiento financiero
- Revisar presupuesto, ingresos y ROI.
- Responder: ¿la inversión genera rentabilidad real?
- Decisión de negocio apoyada: decidir qué tipo de películas o estrategias de producción convienen.

### Sección 5 — Recomendaciones accionables
- Concluir con decisiones concretas para la dirección.
- La narrativa debe terminar en recomendaciones de negocio, no solo en observaciones.

## 8. Wireframe sugerido para Data Studio

Una estructura limpia para el dashboard sería esta:

```text
┌──────────────────────────────────────────────────────────────────────┐
│ FILTROS GLOBALes: Tipo | País | Género | Año | Idioma | Rating       │
├──────────────────────────────────────────────────────────────────────┤
│ KPIs principales                                                     │
│ Total contenidos | Películas | Series | Popularidad media | ROI       │
├──────────────────────────────────────────────────────────────────────┤
│ Mapa / distribución geográfica     │  Top géneros                    │
│ (por país o región)                │  (barras)                      │
├──────────────────────────────────────────────────────────────────────┤
│ Evolución anual                   │  Top títulos populares          │
│ (línea / área)                    │  (ranking)                     │
├──────────────────────────────────────────────────────────────────────┤
│ Rentabilidad financiera           │  Segmento por mercado          │
│ (budget vs revenue / ROI)         │  (comparaciones)               │
├──────────────────────────────────────────────────────────────────────┤
│ Recomendaciones y hallazgos clave                                    │
└──────────────────────────────────────────────────────────────────────┘
```

## 9. Métricas y pantallas recomendadas

### Pantalla 1 — Overview
- Total de contenidos
- Películas vs series
- Países/idiomas
- Popularidad promedio
- top 5 géneros
- objetivo: responder composición general del catálogo

### Pantalla 2 — Mercado y catálogo
- Mapa por país
- Popularidad por región
- distribución por idioma y género
- comparativa de contenido por mercado
- objetivo: responder dónde hay oportunidad de crecimiento

### Pantalla 3 — Rendimiento y calidad
- Popularidad por género
- rating medio por categoría
- top títulos
- series temporales por año
- objetivo: responder qué contenido funciona mejor y en qué contexto

### Pantalla 4 — Financiero
- presupuesto promedio
- ingresos totales
- ROI por película
- comparación de inversión vs retorno
- objetivo: responder si la estrategia financiera es sostenible

## 10. Reproducibilidad y entregables previos a Data Studio

Antes de construir el tablero final, dejar estos artefactos listos:

- dataset limpio y validado en `data/processed/`
- script de limpieza reproducible en `src/etl/initial_cleaning.py`
- documento de metodología en `documentation/markdown/`
- definiciones de KPI en este archivo
- objetivos y audiencia documentados
- wireframe del dashboard listo para pasar a Data Studio
- registro claro de origen de datos, limpieza y filtros aplicados

### 10.1 Cómo se genera el dataset
1. Se toman los CSV originales en `data/`.
2. `src/etl/initial_cleaning.py` ejecuta deduplicación, trim, parseo de fechas y normalización de texto.
3. Se guardan salidas en `data/processed/`.
4. Se genera un resumen de calidad y nulos en `documentation/markdown/`.

### 10.2 Cómo se ejecuta la limpieza
```bash
python src/etl/initial_cleaning.py
```

### 10.3 Cómo se conecta al dashboard
- El dashboard en Data Studio debe conectarse a los CSV ya procesados en `data/processed/`.
- Lo ideal es usar dos fuentes separadas: películas y series, con un campo `type` que permita filtros globales.
- Si se quiere un dashboard más robusto, se recomienda crear una vista unificada o una tabla con campo `type` y columnas comunes, y mantener columnas financieras solo para el subconjunto de películas.

## 11. Guion de defensa final

### Introducción
- “Este dashboard ayuda a decidir dónde invertir en contenido y cómo priorizar mercados según el catálogo disponible.”

### Preguntas clave a responder en la defensa
- ¿Qué problema de negocio resuelve esta visualización?
- ¿Qué audiencia está enfocada?
- ¿Qué métricas son las más relevantes y por qué?
- ¿Qué decisiones de negocio apoyan estas visualizaciones?
- ¿Qué evidencia de datos respalda las recomendaciones?

### Estructura de la defensa
1. Presentar el problema y la audiencia.
2. Mostrar el dashboard y explicar la navegación.
3. Explicar los tres hallazgos clave.
4. Mostrar la lógica detrás de los KPIs escogidos.
5. Cerrar con recomendaciones accionables.

## 12. Siguientes pasos concretos

1. Confirmar la audiencia principal y la decisión que debe apoyar el dashboard.
2. Validar que el dataset queda limpio y documentado.
3. Definir la lista final de KPIs y métricas por pantalla.
4. Preparar el wireframe en Data Studio.
5. Crear la narrativa de análisis para la defensa.
6. Generar el informe final con hallazgos y recomendaciones.

## 13. Conclusión

Lo más importante ahora no es “hacer un dashboard bonito”, sino dejar una base sólida: audiencia definida, KPIs bien elegidos, dataset limpio y una narrativa que convierta datos en decisiones. Con esto ya se puede construir el dashboard en Data Studio sin perder consistencia ni justificación técnica.

## 14. Evaluación final del estado actual

El proyecto ya está preparado para avanzar a la etapa de construcción del dashboard en Data Studio, porque se han cumplido de forma explícita los siguientes bloques:
- audiencia y objetivo definidos
- preguntas de negocio formuladas
- KPI con fórmulas claras por sección
- narrativa de negocio definida
- estructura del dashboard propuesta
- documentación de reproducibilidad y dataset preparada

La única decisión pendiente no bloqueante es determinar si el dashboard prioriza sobre todo contenido y mercado, o si también requiere profundizar en análisis financiero con decisiones de ROI para películas. Ese detalle puede resolverse durante la construcción final en Data Studio sin desordenar la base ya preparada.
