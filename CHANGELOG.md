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
