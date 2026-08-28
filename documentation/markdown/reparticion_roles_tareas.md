---
title: "Repartición de roles y tareas — Equipo de 3"
author: "Equipo StreamView (asistente)"
date: 2026-08-27
source_files:
  - documentation/markdown/reparticion_roles_tareas.md
---

Resumen ejecutivo

Proponemos un equipo de 3 personas con roles complementarios: Data Engineer, Data Analyst / Visual Designer y Product & Insights (reporting y comunicación). Cada rol tiene tareas asignadas por fase y entregables claros.

Roles y responsabilidades

1) Rol: Data Engineer (Persona A)
- Responsabilidades principales:
  - Ingesta y organización de datos (`data/`, `data/processed/`).
  - Limpieza y transformaciones reproducibles (scripts en `src/` o notebooks en `notebooks/`).
  - Preparar tablas/feeds para KPIs y dashboards.
- Tareas por fase:
  - Fase 0: Configurar entorno y estructura de carpetas.
  - Fase 1: Auditoría de calidad, limpieza y documentación (`EP1_data_cleaning.md`).
  - Fase 2: Crear endpoints / CSVs procesados para el dashboard.
  - Fase 3: Automatizar pasos repetibles y compartir scripts con el equipo.
- Entregables: scripts/notebooks, `data/processed/`, `documentation/markdown/EP1_data_cleaning.md`.

2) Rol: Data Analyst / Visual Designer (Persona B)
- Responsabilidades principales:
  - Análisis exploratorio y diseño de visualizaciones.
  - Construcción de KPIs y storytelling inicial.
  - Creación de figuras e imágenes (`images/`) y documentación de decisiones visuales.
- Tareas por fase:
  - Fase 1: EDA, KPIs básicos, primeras visualizaciones y `EP1_informe_ejecutivo.md` (storytelling).
  - Fase 2: Diseñar prototipos visuales, mockups y producir gráficas interactivas.
  - Fase 3: Refinamiento visual, accesibilidad y justificación técnica.
- Entregables: notebooks, imágenes, `documentation/markdown/EP1_informe_ejecutivo.md` y `EP2_visual_design.md`.

3) Rol: Product & Insights / Reporting (Persona C)
- Responsabilidades principales:
  - Definir requerimientos por audiencia (Directorio, Contenidos, Marketing).
  - Implementar la documentación ejecutiva, preparar presentación y coordinar la defensa.
  - Integrar el dashboard con el storytelling y preparar el empaquetado final.
- Tareas por fase:
  - Fase 1: Validar objetivos comunicacionales y público objetivo.
  - Fase 2: Revisión funcional del dashboard, pruebas de usuario y documentación de uso.
  - Fase 4: Preparar presentación ejecutiva, Q&A y empaquetado final.
- Entregables: `EP2_dashboard_documentation.md`, presentación (PPT/PDF), `EFT_package`.

Asignación de tareas concretas (primeras 2 semanas)

- Persona A (Data Engineer): preparar `data/processed/`, script de limpieza y `EP1_data_cleaning.md` (días 1–4).
- Persona B (Analyst/Designer): EDA inicial, 6 gráficos clave y `EP1_informe_ejecutivo.md` (días 3–7).
- Persona C (Product/Insights): redactar objetivos comunicacionales, definir audiencias, revisar entregable EP1 y armar resumen ejecutivo (días 5–7).

Coordinación y entregas

- Reuniones diarias cortas (15 min) para sincronizar progreso.
- Checkpoints: final Semana 1 (EP1 entregable), final Semana 3 (EP2 prototipo).
- Uso de la carpeta `documentation/markdown/` para todos los archivos Markdown y `images/` para figuras.

Notas finales

- Cada tarea debe incluir: archivo fuente (notebook/script), MD con resumen y evidencia (capturas/figuras) y rutas relativas en el YAML de cada MD.
- Ajustar asignaciones si algún miembro tiene restricciones de disponibilidad.
