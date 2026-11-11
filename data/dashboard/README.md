# Carpeta de exports del dashboard

Esta carpeta está destinada a guardar los CSVs optimizados para consumo en Data Studio / Looker Studio y para la capa analítica del dashboard final.

## Archivos esperados

- `dashboard_ejecutivo.csv`: resumen ejecutivo con KPIs y agregaciones por tipo/categoría.
- `dashboard_contenidos.csv`: detalle analítico por contenido, con ranking y comparativas por género/país/idioma.
- `dashboard_predicciones.csv`: predicciones y scores del modelo, para priorización de decisión.

## Regla de uso

- El dashboard descriptivo y el dashboard predictivo deben mantenerse separados por objetivo y sentido analítico.
- `dashboard_ejecutivo` debe centrarse en KPIs y resúmenes.
- `dashboard_contenidos` debe facilitar el análisis de catálogo.
- `dashboard_predicciones` debe apoyar decisiones de adquisición y priorización.

## Nota

Esta carpeta debe contener únicamente artefactos exportados y listos para BI, no notebooks ni código de modelado.
