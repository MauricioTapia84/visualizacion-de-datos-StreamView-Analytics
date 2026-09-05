# Changelog

## En revision

- Resolver 9 pares de registros de TV Shows con el mismo `show_id`, titulo y atributos equivalentes, pero distinto valor de `popularity`.
- La regla pendiente debe definir si se conserva una observacion, como se selecciona su valor de `popularity`, o si se aplica otra consolidacion justificada.
- Hasta contar con esa regla, los 18 registros se conservan para no descartar ni alterar valores de la fuente.

## Preparacion de datos

- Se leyeron `docs/project_brief.md` y `docs/data_rules.md` antes de realizar transformaciones.
- Se cargaron las fuentes oficiales de Movies y TV Shows desde `data/raw/`, sin modificar los archivos originales.
- Se revisaron estructura, valores faltantes, columnas exclusivas y duplicados.
- Se normalizaron espacios iniciales y finales, y los textos vacios se convirtieron en valores nulos.
- Se homologaron las estructuras de ambas fuentes.
- Se incorporaron `budget` y `revenue` al esquema de TV Shows como valores nulos, sin reemplazarlos por cero.
- Se alinearon tipos de datos para identificador, fechas y variables numericas compatibles.
- Se concatenaron Movies y TV Shows verticalmente, sin JOIN ni MERGE.
- Se creo y ejecuto `notebooks/01_limpieza_union.ipynb`.
- Se exporto `data/processed/catalogo_streamview.csv`.
- Se validaron 32.000 filas, presencia de Movie y TV Show, ausencia de filas completamente duplicadas y recarga correcta del CSV exportado.

## Analisis exploratorio basico

- Se creo `notebooks/02_EDA_Catalogo_StreamView.ipynb` como notebook independiente de la limpieza.
- El EDA utiliza `data/processed/catalogo_streamview.csv` como fuente de analisis.
- Se calcularon KPIs de catalogo: contenidos, peliculas, series, paises, idiomas, generos, popularidad y calificacion.
- Se analizaron generos, paises e idiomas mediante tablas derivadas, conservando una fila por contenido en el catalogo maestro.
- Se separaron los rankings de popularidad, generos y paises entre Movies y TV Shows.
- Se incorporo una visualizacion Plotly de popularidad frente a valoracion, usando `vote_count` como contexto del respaldo de las evaluaciones.
- Se calcularon presupuesto promedio, ingresos totales, ROI aproximado y correlacion entre presupuesto e ingresos para peliculas con datos financieros validos.
- Se incorporaron controles de calidad post-limpieza: nulos, duplicados, rangos validos y cobertura financiera.
- Se documentaron los 406 `show_id` repetidos y la cobertura financiera completa de 3.540 peliculas, equivalente a aproximadamente 22,1 % de las peliculas.
- Se generaron prototipos interactivos con Plotly para popularidad, generos, paises, evolucion temporal y finanzas.
- Se exportaron las visualizaciones interactivas como archivos HTML en `images/`.
- Se definio el plan del dashboard en memoria dentro del EDA, sin exportar un CSV auxiliar.
- El EDA mantiene las limitaciones documentadas: `popularity` es un indice relativo, los campos multivalor representan asociaciones y los datos financieros tienen cobertura parcial.
