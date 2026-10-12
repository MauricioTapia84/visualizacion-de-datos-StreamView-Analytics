
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
| Preparación | [notebooks/01_limpieza_union.ipynb](notebooks/01_limpieza_union.ipynb) |
| Análisis exploratorio | [notebooks/02_EDA_Catalogo_StreamView.ipynb](notebooks/02_EDA_Catalogo_StreamView.ipynb) |

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

El EDA reúne las seis visualizaciones interactivas en una sola página:

- [Dashboard interactivo de StreamView](images/dashboard_streamview.html)

Las barras de géneros y países muestran la cantidad de contenidos y el porcentaje sobre el total del tipo correspondiente. Como un contenido puede tener varias asociaciones, esos porcentajes se superponen y no suman 100 %. El ranking de popularidad muestra el índice y los votos, no un porcentaje artificial del índice.

El dashboard HTML integra popularidad, géneros, países, incorporaciones, finanzas y valoración. El dashboard de Looker Studio no está implementado dentro de este repositorio. La siguiente etapa requiere datos propios de reproducciones, usuarios, costos y derechos para validar las hipótesis del EDA.

### CSV único para Looker Studio

Al ejecutar el EDA, `data/processed/catalogo_streamview.csv` se amplía para servir como fuente única de los dashboards: conserva las columnas originales e incorpora nombres legibles en español y 175 indicadores binarios (`genero__...` y `pais__...`), para un total de 207 columnas. Cada fila sigue siendo un contenido. Los campos descriptivos originales `genres` y `country` se conservan y los valores faltantes del archivo final quedan como celdas vacías para facilitar su lectura en herramientas BI.

Los indicadores valen `1` cuando el contenido tiene una asociación y `0` cuando no la tiene. **No se deben sumar entre sí para obtener el total del catálogo**: un contenido puede activar varios géneros y países. Para contar contenidos use `COUNT_DISTINCT(id_contenido)`; `tiene_genero_informado` y `tiene_pais_informado` distinguen la falta de información de una ausencia de asociación. Dirección y reparto se conservan como texto por su alta cardinalidad. Ya no se generan el CSV One-Hot auxiliar ni el diccionario separado.

### Selector de países One-Hot en Looker Studio

El campo original `country` puede contener varios países en una misma celda, por lo que un control desplegable basado directamente en ese campo muestra combinaciones. Para seleccionar un país individual mediante sus indicadores One-Hot:

1. En la fuente de datos de Looker Studio, crea el parámetro `pais_selector` de tipo **Texto**, con valores permitidos de tipo **Lista de valores**.
2. Añade al parámetro los nombres de país como valores permitidos. Deben coincidir exactamente con los nombres de país usados en el campo `CASE` (los nombres de origen están en inglés). Puedes asignar etiquetas en español para mostrar nombres traducidos en el control; el valor interno debe seguir coincidiendo con el `CASE`. Los 147 valores no se generan automáticamente desde el CSV.
3. Añade al informe un control de lista desplegable y establece `pais_selector` como su campo de control.
4. Crea un campo calculado numérico, por ejemplo `pais_seleccionado`, con una condición `WHEN` por país que devuelva su indicador correspondiente (`pais__...`). Usa `ELSE 0` y termina la expresión con `END`. Por ejemplo:

   ```text
   CASE
     WHEN pais_selector = "Canada" THEN pais__canada
     WHEN pais_selector = "Portugal" THEN pais__portugal
     WHEN pais_selector = "United States Of America"
       THEN pais__united_states_of_america
     ELSE 0
   END
   ```

5. Para mostrar el total del país seleccionado, usa la métrica `SUM(pais_seleccionado)`. Para filtrar gráficos o tablas, filtra ese campo por el valor `1`. También se puede contar `id_contenido` con recuento distinto.

Los nombres de las columnas de indicadores están normalizados en minúsculas y guiones bajos; consulta el encabezado del CSV para el nombre exacto de cada campo. Si el parámetro permite cualquier valor en vez de una lista, la persona debe escribir exactamente un valor reconocido por el `CASE`; los valores no contemplados devuelven `0`.

## Herramientas

- Python, Pandas y NumPy
- Jupyter / VS Code
- Plotly para visualizaciones interactivas
- Looker Studio como plataforma prevista para el dashboard
