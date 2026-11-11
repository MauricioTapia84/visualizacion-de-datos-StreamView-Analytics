# Guía de dashboard StreamView Analytics

## 1. Objetivo del dashboard

El dashboard final debe responder dos preguntas de negocio de manera separada pero conectada:

1. ¿Cómo está compuesto el catálogo actual y qué patrones descriptivos emergen? 
2. ¿Qué títulos o categorías tienen mayor potencial de éxito futuro para orientar decisiones de adquisición, renovación y producción?

La vista principal debe estar pensada para el Gerente de Contenidos y Adquisición, con un resumen ejecutivo dirigido al Directorio.

---

## 2. Audiencia y navegación

### Audiencia principal
- Gerente de Contenidos y Adquisición
- Necesita comparar géneros, países, idiomas, tipo de contenido y títulos con potencial de éxito.

### Audiencia secundaria
- Directorio / liderazgo ejecutivo
- Requiere un resumen ejecutivo con KPIs claves y observaciones principales.

### Patrón de navegación recomendado
- Nivel 1: KPIs ejecutivos
- Nivel 2: comparativas por género, país e idioma
- Nivel 3: detalle por título y score predictivo
- Nivel 4: tabla con recomendación y contexto de negocio

---

## 3. Estructura sugerida del dashboard

### Página 1: Resumen ejecutivo
- Total de títulos
- Películas vs series
- Popularidad promedio
- Valoración promedio (`vote_average` filtrada por voto mínimo)
- Países y géneros más relevantes
- % de títulos por nivel de éxito
- KPI de cobertura financiera para películas

### Página 2: Catálogo y composición
- Distribución por tipo (`Movie` / `TV Show`)
- Distribución por género
- Evolución por año de incorporación
- Países y idiomas con mayor presencia
- Tabla de contenido por tipo y formato

### Página 3: Análisis de éxito
- Scatter plot `vote_count` vs `vote_average`
- Ranking por `indice_exito`
- Distribución por categoría `Bajo / Medio / Alto Éxito`
- Comparación de popularidad y valoración por género
- Mapa de desempeño por país con advertencia explícita

### Página 4: Recomendación y priorización
- Ranking de títulos recomendados
- Score predictivo `pred_indice_exito`
- Clase predicha (`Bajo`, `Medio`, `Alto`)
- Variables más relevantes para la decisión
- Tabla con `title`, `type`, `genres`, `country`, `score`, `categoria`, `popularidad`, `valoración`, `votos`

---

## 4. KPIs recomendados

### KPIs ejecutivos
- Total de contenidos
- Películas vs series
- Popularidad promedio
- Valoración promedio con filtro `vote_count >= 100`
- % de títulos en `Alto Éxito`
- % de títulos en `Bajo Éxito`
- ROI aproximado en películas con datos completos

### KPIs de apoyo
- Títulos recomendados para adquisición
- Score promedio del catálogo
- Top 5 géneros por potencial
- Top 10 países / idiomas por valoración
- Cobertura financiera estimada por película

---

## 5. Reglas de negocio que deben estar visibles en el dashboard

- `vote_average` debe mostrarse con advertencia si se usa sin filtro de respaldo.
- `popularity` debe etiquetarse como indicador relativo y no como reproducción real.
- `budget` y `revenue` solo deben usarse para películas y con contexto de cobertura parcial.
- Las decisiones de visualización deben mantener claro que el modelo no reemplaza la decisión humana.
- Las categorías de éxito deben ser interpretadas como priorización de riesgo y oportunidad, no como verdad absoluta.

---

## 6. Visualizaciones recomendadas

### Barras
- Géneros por presencia
- Países por presencia
- Idiomas por presencia
- Ranking de títulos por `indice_exito`

### Líneas
- Evolución temporal por incorporación o estreno
- Tendencia de popularidad por año

### Dispersión
- `vote_count` vs `vote_average`
- `budget` vs `revenue` (solo películas)
- `popularidad` vs `valoración` para títulos candidatos

### Tablas
- Ranking de títulos por score
- Evolución de priorización por categoría
- Tabla de contenidos recomendados para adquisición

---

## 7. Recomendación de diseño para DataStudio

- Utilizar un esquema visual claro y sobrio: fondo blanco, acentos azules y tonos neutros.
- Mantener KPI principal arriba y granularidad debajo.
- Separar la vista ejecutiva de la vista analítica.
- Usar filtros globales: `type`, `genre`, `country`, `language`, `year`, `category`.
- Añadir restos de contexto y anotaciones con reglas de negocio en el pie del dashboard.
- Evitar saturar la vista con demasiadas dimensiones simultáneas.

---

## 8. Estructura de archivos esperados para el entregable final

```text
data/
  dashboard/
    dashboard_ejecutivo.csv
    dashboard_contenidos.csv
    dashboard_predicciones.csv
    README.md

images/
  dashboard_streamview.html
  mockup_dashboard_baja_fidelidad.html

models/
  best_regression_model.pkl
  best_classifier_model.pkl
```

---

## 9. Criterio de éxito del dashboard

El dashboard se considerará listo cuando:

- muestre claramente el catálogo y su composición,
- permita diferenciar por `type`, `genre`, `country`, `language` y `year`,
- integre una capa predictiva con score y categoría,
- deje visible la advertencia sobre la calidad de los datos y la naturaleza relativa de `popularity`,
- sirva como apoyo a decisiones de adquisición y renovación, no solo como vista descriptiva.

### Reglas de mejora añadidas para la Etapa 3

- Priorizar un dashboard orientado a la decisión de adquisición y renovación, no a la mera descripción del catálogo.
- Usar `vote_average` y `vote_count` como contexto conjunto para cualquier análisis de valoración.
- Aplicar un filtro mínimo de `vote_count >= 100` para evitar comparaciones engañosas.
- Diferenciar claramente entre tendencias de catálogo y métricas de calidad de contenido.
- Mostrar el panel de éxito con una vista ejecutiva y otra analítica.
- Incluir advertencias visibles sobre popularidad relativa y cobertura parcial de `budget` / `revenue`.

---

## 10. Conclusión

El dashboard debe ser un sistema de decisión, no solo un panel de reportes. La clave está en combinar la capacidad descriptiva del catálogo con una priorización accionable basada en `indice_exito`, validación de calidad y reglas de negocio explícitas.
