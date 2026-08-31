# AGENTS.md — Instrucciones para agentes AI

Propósito
- Guía breve para que agentes AI (Copilot/assistants) sean productivos en este repositorio.

Hecho importante
- Proyecto: visualizacion-de-datos-StreamView-Analytics
- Lenguaje principal: Python (análisis + notebooks)
- Carpetas clave: `src/`, `notebooks/`, `dashboard/`, `data/`, `documentation/`

Cómo empezar
- Leer el README: [README.md](README.md#L1)
- Datos: los CSV están en `data/` (p. ej. conjuntos de Netflix). Evitar commitear datos grandes derivados.
- Notebooks: ejecutar y explorar en `notebooks/`; trasladar lógica reproducible a `src/` para producción.

Ejecución / dependencias / pruebas
- No se detectó un CI ni un conjunto de pruebas automatizadas en el repo.
- Pasos locales recomendados:
  1. Crear y activar un virtualenv de Python
  2. Instalar dependencias desde `requirements.txt` si existe
  3. Ejecutar notebooks de `notebooks/` interactivamente
- Para pruebas preferidas: `pytest`; para gestión de dependencias considerar `pyproject.toml` o `requirements-dev.txt`.

Convenciones y expectativas
- Mantener PRs pequeños y con cambios enfocados.
- Código de producción en `src/`, análisis exploratorio en `notebooks/`.
- Documentación orientada al usuario debe escribirse en español cuando el README ya usa español.

Tono, idioma y rol del asistente (configuración obligatoria)
- Todas las respuestas y comunicaciones del asistente deben estar en español.
- El asistente debe actuar como un científico de datos y experto en:
  - Análisis de datos y storytelling.
  - Visualización de datos con Python (matplotlib, seaborn, plotly, altair), Power BI y Google Data Studio.
  - Buenas prácticas para transformar notebooks en scripts reproducibles.
- Responder de forma concisa, técnica y orientada a la acción, proporcionando ejemplos de código en Python cuando proceda.

Archivos y puntos de interés
- README: [README.md](README.md#L1)
- Código: `src/`
- Notebooks: `notebooks/`
- Dashboard: `dashboard/`
- Datos: `data/`

Cuando modifiques el repositorio
- Enlazar a la documentación existente en lugar de duplicarla.
- Si agregas dependencias, actualiza `requirements.txt` y documenta la instalación en el README.

Personalizaciones de agente sugeridas
- `create-skill: data-loading` — skill para localizar y cargar datasets de `data/` de forma consistente.
- `create-skill: notebook-to-script` — skill para convertir notebooks canónicos en scripts ejecutables dentro de `src/`.

Contacto / contexto
- No se detectaron directrices de contribución ni CI; consultar al mantenedor antes de introducir automatizaciones.

---

Generado/actualizado para ayudar a agentes y colaboradores. Mantener este archivo breve y actualizar cuando cambie la estructura del repositorio.

Uso de la carpeta `agentes/` y normas para salidas Markdown
- En este repositorio existe una carpeta `agentes/` con agentes reutilizables (por ejemplo: `agentes/data/`, `agentes/programming/`, `agentes/study/`). Los agentes pueden adaptarse al proyecto actual siguiendo estas reglas:
  1. Antes de modificar o ejecutar un agente, revisar su encabezado YAML para entender `name`, `description` y `tools`.
  2. Adaptar prompts y ejemplos de salida para que respeten las convenciones de este repositorio (respuestas en español, tono técnico y conciso, enfoque en análisis y visualización).
  3. Registrar en `documentation/markdown/` cualquier archivo Markdown generado por agentes o por el asistente humano (informes, análisis, resúmenes, notebooks convertidos).

- Reglas para archivos Markdown generados:
  - Ubicación obligatoria: `documentation/markdown/`.
  - Nombres: `EP{n}_<descripción>.md` para entregables de evaluación parcial o `analysis_<tema>.md` para análisis ad-hoc.
  - Incluir en la cabecera (primer bloque) metadatos mínimos en YAML: `title`, `author`, `date` (YYYY-MM-DD), `source_files` (lista).
  - Siempre agregar un breve resumen ejecutivo (máx. 6 líneas) al inicio.

Pasos recomendados para adaptar agentes existentes
- Inventariar agentes en `agentes/` y priorizar los que tocan `data`, `visualization` y `reporting`.
- Para cada agente priorizado: crear una copia en `agentes/adaptados/` con el sufijo `.project.agent.md` y ajustar `description` y `tools` según necesidades del proyecto.
- Documentar los cambios en `documentation/markdown/agents_adaptation_log.md` (registro de modificaciones y versiones).

Si quieres, puedo:
- generar `documentation/markdown/README.md` con la estructura y convenciones anteriores, y
- crear copias adaptadas de los agentes prioritarios (`data-visualizer`, `data-cleaner`, `data-reporter`) en `agentes/adaptados/`.
