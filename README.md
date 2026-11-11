
# StreamView Analytics: Informe ejecutivo

Proyecto académico de Visualización de Datos que integra y explora un catálogo de películas y series para apoyar decisiones de contenido y marketing. Los datos son una colección externa de Netflix detallada hasta 2025; no representan reproducciones, usuarios ni resultados operativos propios de StreamView.

## Resumen ejecutivo

El catálogo integrado contiene **32.000 registros y 15 variables**: 16.000 películas y 16.000 series. Movies y TV Shows se homologan y se unen verticalmente con `pandas.concat`; no se utiliza `merge` ni `join`. El análisis es descriptivo y no incluye modelo predictivo ni división train/test.

Los principales hallazgos son una cobertura temática de 28 géneros, 147 países y 83 idiomas; mayor presencia del género Drama y de Estados Unidos; y cobertura financiera completa para solo 3.540 películas (22,1 %). La popularidad es un índice relativo de la fuente, no una medida de audiencia de StreamView.

## Fuentes y método

| Elemento | Descripción |
|---|---|
| Películas | `data/raw/netflix_movies_detailed_up_to_2025.csv` |
| Series | `data/raw/netflix_tv_shows_detailed_up_to_2025.csv` |
| Dataset analítico | `data/processed/catalogo_streamview.csv` |
| Unidad de análisis | Una fila por contenido audiovisual |
| Integración | Homologación de columnas y concatenación vertical con `pd.concat(..., ignore_index=True)` |
| Preparación | [notebooks/01_eda_y_limpieza.ipynb](notebooks/01_eda_y_limpieza.ipynb) |
| Modelado predictivo | [notebooks/02_modelado_predictivo.ipynb](notebooks/02_modelado_predictivo.ipynb) |

El campo `type` distingue `Movie` de `TV Show`. Antes de concatenar, se alinean los esquemas y se añaden `budget` y `revenue` a las series como valores no aplicables. Las filas completamente duplicadas se detectan y eliminan durante la limpieza de cada fuente. Después de integrar, se excluyen `show_id`, `duration` y `description` del catálogo analítico.

## Nulos y calidad

Los valores faltantes se conservan y se representan como `numpy.nan`. Las cadenas vacías y los textos compuestos por espacios se normalizan a ese valor. El CSV se exporta con `NaN` explícito y se recarga comprobando que vuelve a `np.nan`. No se imputan datos automáticamente.

Los ceros de `budget` y `revenue` se interpretan como información financiera no disponible y se convierten en `NaN`. Para las series, ambas variables son no aplicables y permanecen nulas. La moneda de los campos financieros no está especificada en la documentación disponible.

| Control | Resultado |
|---|---:|
| Filas y columnas | 32.000 × 15 |
| Películas / series | 16.000 / 16.000 |
| Filas completamente duplicadas en el resultado | 0 |
| Valores fuera de los rangos revisados | 0 |
| Celdas faltantes | 69.310 |
| Nulos en `budget` / `revenue` | 27.153 / 26.355 |
| Películas con presupuesto e ingresos disponibles | 3.540 (22,1 % de las películas) |

La falta de datos financieros es alta: falta presupuesto en 84,85 % de las filas e ingresos en 82,36 %. El conteo total incluye series, donde esas variables no aplican. Entre las variables descriptivas, faltan director en 34,68 %, país en 7,07 %, reparto en 4,25 % y género en 3,38 % de los registros.

## Hallazgos del EDA

| Dimensión | Hallazgo |
|---|---|
| Periodo de incorporación | 2010–2025; corresponde a la fecha de alta en la fuente, no al año de estreno. |
| Diversidad del catálogo | 28 géneros, 147 países y 83 códigos de idioma. |
| Género más asociado | Drama: 7.862 series y 6.910 películas. Las categorías multivalor se superponen. |
| País más asociado | Estados Unidos: 7.762 películas y 3.194 series. Un contenido puede estar asociado a más de un país. |
| Señales promedio | Índice de popularidad 42,62 y valoración promedio 5,69/10. |
| Serie con mayor popularidad relativa en el ranking | *The Late Show with Stephen Colbert*: 6.421,92 de popularidad y 288 votos. |
| Película con mayor popularidad relativa en el ranking | *The Gorge*: 3.876,01 de popularidad y 1.572 votos. |

La popularidad es relativa a la fuente y no equivale a visualizaciones, reproducciones o usuarios. La valoración debe leerse junto con la cantidad de votos. Estos datos permiten explorar el catálogo, pero no medir consumo real de StreamView.

### Finanzas de películas

El análisis financiero se limita a las **3.540 películas** con presupuesto e ingresos disponibles. En ese subconjunto, el presupuesto promedio es **35.582.138 unidades de la fuente**, los ingresos suman **367.371.433.138 unidades de la fuente**, el ROI aproximado mediano es **0,70 (70 %)** y la correlación presupuesto-ingresos es **0,748**. No se conoce la moneda y estas cifras no representan ingresos, costos ni rentabilidad de StreamView.

### Segmentos para investigar

El indicador exploratorio de oportunidad destaca series asociadas con **Portugal** (86 contenidos; popularidad media 183,43; participación aproximada 0,3 %) y **Sudáfrica** (56 contenidos; 183,11; 0,2 %). Son hipótesis para investigación, no evidencia de demanda ni recomendaciones automáticas de adquisición; deben contrastarse con audiencia propia, derechos, costos y competencia.

## Dashboard y estado

El proyecto mantiene dos capas complementarias:

- capa descriptiva del catálogo y comportamiento del contenido,
- capa predictiva para priorización de adquisiciones y renovación con `indice_exito` y categorías `Bajo/Medio/Alto Éxito`.

El dashboard HTML base disponible en la carpeta `images/` sirve como referencia visual y validación del flujo, mientras que la capa final BI queda preparada para exportar CSVs optimizados desde el pipeline.

### Estado real del proyecto

El repositorio ya dispone de:

- base analítica limpia y unificada en `data/processed/catalogo_streamview.csv`,
- split train/test exportado en `data/processed/train_procesado.csv` y `data/processed/test_procesado.csv`,
- modelos entrenados en `models/`,
- script reproducible en `src/pipeline/fase_4_dashboard.py`,
- guía documental para el dashboard y la arquitectura del proyecto en `docs/`.

La entrega BI final requiere cerrar la exportación definitiva de los CSVs de dashboard en `data/dashboard/` y ajustar la guía de implementación de Data Studio a la estructura final del proyecto.

### Estructura final esperada del entregable

```text
data/
  processed/
    catalogo_streamview.csv
    train_procesado.csv
    test_procesado.csv
  dashboard/
    dashboard_ejecutivo.csv
    dashboard_contenidos.csv
    dashboard_predicciones.csv
    README.md
models/
  best_regression_model.pkl
  best_classifier_model.pkl
images/
  dashboard_streamview.html
  mockup_dashboard_baja_fidelidad.html
```

### Reglas clave de negocio para el dashboard

- `vote_average` debe interpretarse con filtro mínimo de votos.
- `popularity` es un índice relativo de la fuente, no un indicador de reproducciones reales.
- `budget` y `revenue` solo aplican a películas y no representan rentabilidad real de StreamView.
- El modelo sirve para apoyar decisiones, no para reemplazar la capacidad de análisis humano.

## Documentación de mejoras y entregables

El proyecto ya incorpora la línea de trabajo de mejora de la Etapa 3 y el apoyo para la defensa del proyecto:

- [docs/documento_maestro_mejoras_streamview.md](docs/documento_maestro_mejoras_streamview.md): consolidación de correcciones, reglas de negocio y mejora del dashboard.
- [docs/guia_dashboard_datastudio.md](docs/guia_dashboard_datastudio.md): guía de diseño, estructura y navegación del dashboard final.
- [docs/instrucciones_actualizacion_dashboard_informe_ppt_fase3.md](docs/instrucciones_actualizacion_dashboard_informe_ppt_fase3.md): instrucciones concretas para actualizar el mockup, redactar el informe de fase 3 y preparar la presentación PPT 3.

## Herramientas

- Python, Pandas y NumPy
- Jupyter / VS Code
- Plotly para visualizaciones interactivas
- Looker Studio como plataforma prevista para el dashboard
