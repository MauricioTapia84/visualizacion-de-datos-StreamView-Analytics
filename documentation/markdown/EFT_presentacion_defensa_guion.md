---
title: "EFT — Guion de presentación y defensa"
author: "Equipo StreamView"
date: 2026-08-28
source_files:
  - documentation/markdown/analysis_eda_catalogo.md
  - documentation/markdown/EP2_dashboard_documentation.md
  - notebooks/EP1_eda_catalogo.ipynb
---

## Secuencia de presentación

1. **Problema:** StreamView necesita convertir el catálogo en decisiones de adquisición, contenidos y marketing.
2. **Datos y método:** 32.000 contenidos, limpieza reproducible, separación de dimensiones múltiples y exclusión financiera explícita.
3. **Hallazgo de catálogo:** Drama domina; la oferta se concentra en pocos países y géneros.
4. **Hallazgo de interés:** la popularidad es relativa y debe leerse junto a valoración y número de votos.
5. **Hallazgo financiero:** correlación budget-revenue de 0,730, pero ROI mediano de -22,2%; correlación no implica rentabilidad.
6. **Decisión:** usar dashboard con vistas separadas por tipo, filtros y descarga.
7. **Cierre:** validar oportunidades latinoamericanas con demanda, costos y competencia antes de invertir.

## Preguntas para defensa

- ¿Por qué no usar un gráfico de composición? Porque el KPI responde la proporción sin aportar profundidad adicional.
- ¿Por qué separar películas y series? Evita que volumen, escalas y títulos de una categoría oculten a la otra.
- ¿Por qué usar logaritmos en finanzas? Presupuesto e ingresos abarcan órdenes de magnitud distintos.
- ¿Qué limitación es crítica? `popularity` no es reproducciones y el dataset no contiene demanda de usuarios.
- ¿Cómo se reproduce? Ejecutar limpieza, luego EDA y finalmente `streamlit run dashboard/app.py`.
