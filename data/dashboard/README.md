# Fuentes de datos del dashboard

La capa final y reproducible para Looker Studio se genera desde los CSV originales ejecutando:

```bash
python3 src/pipeline/fuentes_dashboard_finales.py
```

## Fuentes finales

- `dashboard_contenidos_final.csv`: una fila por contenido; fuente principal del dashboard.
- `dashboard_generos.csv`: una fila por relación contenido-género; fuente para rankings y análisis de géneros.
- `dashboard_paises.csv`: una fila por relación contenido-país; fuente para mapas y análisis geográfico.

El detalle de filas, columnas, identificadores, nulos, cobertura financiera y checks se encuentra en `dashboard_validation.json` y `dashboard_validation.md`. La descripción reproducible del proceso está en `README_fuentes_finales.md`.

## Identificadores y finanzas

`id_contenido` se construye desde `type` y `show_id`. Si el par se repite, se añade un hash determinista de la fila original; nunca se usa un número secuencial dependiente del orden.

`budget` y `revenue` se conservan únicamente para Movies, se renombran como `presupuesto` e `ingresos`, y los ceros interpretados como ausencia se exportan como NULL/campo vacío. TV Shows queda siempre sin valores financieros válidos.

## Modelado experimental

Los archivos históricos `dashboard_contenidos.csv`, `dashboard_predicciones.csv` y `dashboard_ejecutivo.csv` se mantienen separados de la capa final. El modelado predictivo no se elimina, pero sus predicciones no forman parte de `dashboard_contenidos_final.csv`.
