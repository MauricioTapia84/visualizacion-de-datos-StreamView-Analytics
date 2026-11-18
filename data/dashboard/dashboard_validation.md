# Validación de fuentes finales para Looker Studio

Estado: **PASS**

## Salidas

| Archivo | Filas | Columnas | IDs únicos | Duplicados de ID | Nulos por campo |
|---|---:|---:|---:|---:|---|
| `dashboard_contenidos_final.csv` | 32000 | 12 | 32000 | 0 | `{'id_contenido': 0, 'titulo': 0, 'tipo': 0, 'generos': 1081, 'pais': 2263, 'idioma': 0, 'anio_publicacion': 0, 'popularidad': 0, 'votos': 0, 'valoracion_promedio': 0, 'presupuesto': 27153, 'ingresos': 26355}` |
| `dashboard_generos.csv` | 65900 | 9 | 30919 | 34981 | `{'id_contenido': 0, 'genero_individual': 0, 'tipo': 0, 'popularidad': 0, 'votos': 0, 'valoracion_promedio': 0, 'anio_publicacion': 0, 'idioma': 0, 'pais': 2631}` |
| `dashboard_paises.csv` | 37636 | 9 | 29737 | 7899 | `{'id_contenido': 0, 'pais_individual': 0, 'tipo': 0, 'popularidad': 0, 'votos': 0, 'valoracion_promedio': 0, 'anio_publicacion': 0, 'idioma': 0, 'generos': 484}` |

## Identificador

`show_id` combinado único: **31594** de 32000 filas.
Colisiones entre tipos: **397**.
Valores base duplicados dentro de un mismo tipo: **9**.

Los IDs normales usan `Movie_<show_id>` o `TV_<show_id>`. Cuando el par tipo/show_id se repite, se añade un fragmento determinista de SHA-256 de la fila original; no se usa el orden de las filas.

## Finanzas

- Movies con presupuesto informado: **4847**.
- Movies con ingresos informados: **5645**.
- Movies con ambos campos informados: **3540**.
- Cobertura de ambos campos sobre 16.000 Movies: **22.125%**.
- TV Shows con presupuesto válido: **0**.
- TV Shows con ingresos válidos: **0**.
- Ceros de origen convertidos a NULL: `{'revenue': 10355, 'budget': 11153}`.

## Top 10 por contenido distinto

### Géneros

| Género | COUNT DISTINCT id_contenido |
|---|---:|
| Drama | 14772 |
| Comedy | 9109 |
| Animation | 4069 |
| Thriller | 3769 |
| Action | 3239 |
| Crime | 3203 |
| Family | 3014 |
| Mystery | 2575 |
| Romance | 2571 |
| Horror | 2425 |

### Países

| País | COUNT DISTINCT id_contenido |
|---|---:|
| United States of America | 10956 |
| Japan | 2871 |
| United Kingdom | 2609 |
| China | 2399 |
| South Korea | 2174 |
| France | 2108 |
| Canada | 1716 |
| Germany | 1160 |
| India | 912 |
| Spain | 822 |

## Checks

| Validación | Resultado |
|---|---|
| `source_has_32000_rows` | PASS |
| `source_has_16000_movies` | PASS |
| `source_has_16000_tv_shows` | PASS |
| `content_has_exactly_32000_rows` | PASS |
| `content_has_one_row_per_content` | PASS |
| `content_has_no_duplicate_ids` | PASS |
| `content_has_required_columns_only` | PASS |
| `content_has_no_predictive_columns` | PASS |
| `genre_relations_have_no_duplicates` | PASS |
| `country_relations_have_no_duplicates` | PASS |
| `tv_shows_have_no_valid_budget` | PASS |
| `tv_shows_have_no_valid_revenue` | PASS |
| `financial_zeros_are_not_exported_as_zero` | PASS |
| `all_source_rows_have_show_id` | PASS |
| `all_output_ids_are_unique` | PASS |

## Alcance predictivo

Las predicciones experimentales existentes no se incluyen en esta capa. El pipeline predictivo actual predice las 32000 filas completas, mezclando filas usadas en entrenamiento y prueba; además, indice_exito se construye con variables que también se entregan al modelo.

Los artefactos predictivos existentes se mantienen fuera de `dashboard_contenidos_final.csv`.
