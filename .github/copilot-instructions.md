# Instrucciones de Copilot para StreamView Analytics

## Visión general del proyecto
- Este repositorio corresponde a un proyecto de análisis de datos y visualización centrado en el catálogo de Netflix y en la creación de dashboards.
- El flujo principal del proyecto es: CSVs originales en `data/` -> notebooks de exploración en `notebooks/` -> lógica reutilizable en Python en `src/` -> informes generados en `documentation/markdown/`.
- La lógica de producción debe quedarse en `src/`, mientras que el trabajo exploratorio y analítico se mantiene en notebooks.

## Mapa del repositorio
- `data/`: datasets originales y archivos procesados generados. Mantener los CSV originales intactos y evitar subir derivados innecesariamente grandes.
- `notebooks/`: notebooks de análisis exploratorio y EDA (`EP1_eda_catalogo.ipynb`, `EP1_initial_cleaning_colab.ipynb`).
- `src/`: código Python reutilizable. Actualmente incluye lógica ETL/preprocesamiento en `src/etl/initial_cleaning.py`.
- `documentation/markdown/`: informes, análisis y documentación generada, con metadatos YAML al inicio de los archivos Markdown.
- `README.md` y `AGENTS.md` son las guías principales de referencia del repositorio.

## Comandos de compilación, pruebas y lint
- Preparación del entorno:
  - `python -m venv .venv`
  - Windows: `.venv\Scripts\activate`
  - macOS/Linux: `source .venv/bin/activate`
  - `pip install -r requirements.txt`
- No hay un pipeline de build ni configuración de lint integrada en este repositorio.
- No existe una suite automatizada de pruebas en el repo en este momento.
- Si más adelante se agrega pytest, la forma recomendada para ejecutar una prueba concreta es:
  - `pytest`
  - `pytest path/to/test_file.py`
  - `pytest path/to/test_file.py -k "test_name"`
- El flujo de validación actual del proyecto es basado en scripts: ejecutar el ETL/preprocesamiento desde la raíz del repositorio:
  - `python src/etl/initial_cleaning.py`
- El trabajo en notebooks debe validarse ejecutando el notebook relevante o reproduciendo los pasos en un script dentro de `src/` si la lógica va a reutilizarse.

## Arquitectura y flujo de datos
- El proyecto está organizado alrededor de limpieza de datos y análisis exploratorio, no de una aplicación web o servicio con API.
- El script ETL en `src/etl/initial_cleaning.py` lee CSVs raw desde `data/`, elimina duplicados, normaliza espacios, parsea fechas y maneja nulos, y luego escribe archivos procesados en `data/processed`.
- El mismo script genera un informe Markdown con front matter YAML en `documentation/markdown/`, en línea con la convención del repositorio para entregables generados.
- Se debe priorizar la reproducibilidad: preferir workflows basados en scripts por sobre ediciones puntuales en notebooks cuando la lógica se reutilizará o compartirá.

## Convenciones clave
- Usar scripts en Python para cualquier tarea que necesite ejecutarse varias veces o reutilizarse; dejar notebooks enfocados en exploración y narrativa visual.
- Usar rutas relativas al repositorio en lugar de rutas absolutas del equipo o la máquina local.
- Mantener la documentación y los mensajes dirigidos a usuarios en español, dado que el repositorio ya está en español.
- Los documentos Markdown generados deben seguir la convención de `documentation/markdown/README.md`:
  - front matter YAML con `title`, `author`, `date` y `source_files`
  - resumen ejecutivo breve justo después del encabezado
  - nombres como `EP{n}_<descripción>.md` o `analysis_<tema>.md`
- Si se agregan dependencias, actualizar `requirements.txt` y documentar la instalación en `README.md` o en la documentación relevante.
- Mantener cambios pequeños y enfocados; evitar refactors amplios para tareas puntuales de análisis o limpieza de datos.

## Hábitos de trabajo para Copilot
- Antes de escribir lógica, comprobar si ya existe una implementación similar en `src/` o si corresponde extraerla desde un notebook.
- Al modificar scripts de procesamiento, mantener el comportamiento determinista y fácil de ejecutar desde la raíz del repositorio.
- Al generar informes o análisis, ubicarlos en `documentation/markdown/` y seguir el patrón de front matter existente.
- Si un flujo es exclusivo de notebook, dejarlo en `notebooks/` a menos que sea claramente un activo reutilizable de producción.

## Reglas de documentación y entrega
- Cuando se genere documentación técnica o resultados del análisis, colocarlos en `documentation/markdown/` y mantener el mismo estilo del repositorio.
- Las entregas deben ser concisas, técnicas y alineadas con el caso del proyecto de visualización de datos.
- Las referencias a datasets deben hacerse con rutas relativas a `data/` y evitando paths locales específicos del entorno.

## Recomendaciones para futuras sesiones
- Revisar primero `README.md`, `AGENTS.md` y cualquier script relevante en `src/` antes de introducir cambios grandes.
- Priorizar lógica reproducible y bien estructurada sobre análisis ad hoc en notebooks.
- Mantener pequeños PRs y cambios centrados en la tarea en curso.
