
# StreamView Analytics - Project Brief 

## Proyecto

Proyecto académico de la asignatura Visualización de Datos.

El proyecto busca desarrollar una solución de Visual Analytics para
StreamView Analytics utilizando información de su catálogo audiovisual.

## Problema de negocio

StreamView Analytics dispone de información relevante sobre películas
y series, pero no cuenta con una visión integrada del catálogo que
facilite su interpretación y utilización para la toma de decisiones.

## Audiencias

La solución está orientada principalmente a:

- Directorio.
- Gerencia de Contenidos y Adquisición.
- Gerencia de Marketing.

## Fuentes de datos

Los datos oficiales se encuentran en:

- data/raw/netflix_movies_detailed_up_to_2025.csv
- data/raw/netflix_tv_shows_detailed_up_to_2025.csv

## Alcance técnico actual

En esta etapa se debe realizar únicamente:

1. Carga de ambas fuentes.
2. Revisión necesaria para realizar la limpieza.
3. Limpieza de los datos.
4. Homologación de las estructuras necesarias.
5. Unión de Movies y TV Shows.
6. Exportación del dataset integrado.

El resultado debe almacenarse en:

data/processed/catalogo_streamview.csv

## Fuera del alcance actual

Todavía NO corresponde:

- análisis exploratorio;
- selección definitiva de visualizaciones;
- storytelling;
- construcción del dashboard;
- conclusiones de negocio;
- recomendaciones.

Los dashboards serán desarrollados posteriormente en Looker Studio
(Data Studio).

## Herramientas

- Python / Pandas para preparación de datos.
- Jupyter Notebook o VS Code para ejecución.
- Looker Studio para visualización y dashboards.
