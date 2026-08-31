---
title: "EP3 — Protocolo de usabilidad y evaluación crítica"
author: "Equipo StreamView"
date: 2026-08-28
source_files:
  - dashboard/app.py
  - documentation/markdown/EP2_dashboard_documentation.md
---

## Estado

El dashboard funcional ya está implementado. La prueba con usuarios reales queda pendiente de ejecución y no se presenta como evidencia realizada.

## Protocolo

Aplicar una prueba de 15 minutos a una persona de cada audiencia:

1. Directorio: encontrar el tipo de contenido con mayor valoración y explicar una decisión de inversión.
2. Contenidos: comparar géneros de películas y series para detectar una oportunidad.
3. Marketing: localizar el top de popularidad de un tipo y descargar el resultado filtrado.

Registrar tiempo, errores, dudas y comentario final. Criterio de aceptación: completar cada tarea en menos de 3 minutos, sin ayuda, con al menos 4/5 en claridad.

## Evaluación crítica inicial

Fortalezas: comparación por tipo, filtros simples, tooltips, exportación y advertencias metodológicas.
Riesgos: la popularidad no representa reproducciones, la línea temporal del dataset es plana y el proxy de mercados no mide demanda.
Mejoras siguientes: añadir mapa geográfico, filtro de género/país, accesibilidad con contraste verificado y feedback real.
