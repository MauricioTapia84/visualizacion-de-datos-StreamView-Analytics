---
title: "Checklist de cumplimiento — EDA, caso y rúbrica StreamView"
author: "Equipo StreamView — revisión Data Analyst / Visual Designer"
date: 2026-08-28
source_files:
  - notebooks/EP1_eda_catalogo.ipynb
  - documentation/markdown/caso_semestral_resumen.md
  - documentation/markdown/rubrica_pautas_resumen.md
  - documentation/markdown/analysis_eda_catalogo.md
---

## Resumen ejecutivo

El EDA cubre los KPIs y preguntas principales del caso y está ejecutado con resultados reproducibles.
Se añadieron auditorías de rangos, cobertura financiera, percentiles, tablas por tipo,
dashboard funcional, documentación y guion de defensa. El proyecto aún requiere ejecución humana
de pruebas de usabilidad, exportación/revisión de PDF y defensa oral.

## Estados

- **[x] Cumplido:** existe evidencia ejecutada y documentada.
- **[~] Parcial:** existe una aproximación, pero falta evidencia, precisión o implementación.
- **[ ] Pendiente:** todavía no está realizado.

## 1. Requisitos del caso de estudio

| Estado | Requisito | Evidencia actual | Acción para cerrar |
|---|---|---|---|
| [x] | Total de contenidos | 32.000 registros calculados | Mantener KPI en el informe y dashboard |
| [x] | Películas y series | 16.000 películas y 16.000 series | Mostrar como KPI, no necesariamente como gráfico |
| [x] | Países, idiomas y géneros | 147 países, 83 idiomas y 28 géneros | Mantener tablas exportadas y filtros posteriores |
| [x] | Géneros predominantes | Drama, Comedy y Animation identificados | Añadir porcentajes sobre el total por tipo |
| [x] | Contenidos más populares | Top 10 separado para películas y series | Añadir control de número de votos para contextualizar |
| [x] | Popularidad por género | Promedio de popularidad y `generos_por_tipo.csv` | Usar filtros del dashboard |
| [x] | Popularidad por país | Promedio de popularidad y `paises_por_tipo.csv` | Usar filtros del dashboard |
| [x] | Calificación promedio | KPI general y promedios por género/país | Interpretar junto con votos |
| [x] | Presupuesto promedio | Calculado sobre películas válidas | Mostrar fórmula y moneda/unidad del dataset |
| [x] | Ingresos totales | Calculado sobre películas válidas | Mostrar fórmula y criterios de inclusión |
| [x] | ROI aproximado | ROI mediano de -22,2% | Documentar que no es ROI de StreamView ni rentabilidad causal |
| [x] | Relación budget-revenue | Correlación 0,730 y dispersión logarítmica | Añadir línea de referencia y análisis de valores extremos |
| [x] | Periodo y alcance | Incorporaciones 2010-2025 documentadas | Mantenerlo visible en títulos o subtítulos |
| [x] | Restricción financiera | Solo películas con datos válidos y `budget > 0` | Añadir conteo de excluidos y porcentaje de cobertura |
| [x] | Interpretación de popularity | Se aclara que es índice relativo | Repetir la advertencia en dashboard y presentación |
| [~] | Mercados prioritarios | Proxy con mínimo de 30 contenidos y mercados LATAM | Validar demanda real, costos y competencia; no presentarlo como predicción |
| [x] | Evolución temporal | Paneles separados y línea interactiva por tipo | Documentar que 1.000 por tipo/año es una limitación del dataset |

## 2. Calidad y reproducibilidad del EDA

| Estado | Requisito | Evidencia actual | Acción para cerrar |
|---|---|---|---|
| [x] | Notebook separado de limpieza | `EP1_eda_catalogo.ipynb` lee `data/processed/` | Conservar el orden de ejecución documentado |
| [x] | Rutas reproducibles | Resuelve raíz desde `notebooks/` | Probar también desde la raíz del repositorio |
| [x] | Detección de archivos faltantes | Lanza `FileNotFoundError` | Mantener mensaje de ejecución previa |
| [x] | Transformación de géneros, países e idiomas | Función de explosión sin duplicar KPI de catálogo | Documentar claramente unidades de análisis |
| [x] | Control de nulos y duplicados | KPI de nulos totales y duplicados; detalle en limpieza | Incorporar tabla por columna al informe EDA |
| [x] | Validación de tipos y rangos | Auditoría exportada; cero valores inválidos | Mantener la auditoría al regenerar |
| [x] | Control de valores extremos | Percentiles financieros p01-p99 exportados | Revisar visualmente outliers al presentar |
| [x] | Tablas exportables | Nueve CSV en `data/processed/` | Mantener nombres y rutas estables |
| [x] | Figuras exportables | Cinco figuras comparativas en `images/` | No volver a mezclar figuras obsoletas |
| [x] | Resultados completamente regenerables | El notebook genera tablas, figuras, matriz e informe | Ejecutar desde entorno limpio como control final |

## 3. Cobertura de la rúbrica resumida

| Estado | Indicador o criterio | Evidencia actual | Acción para alcanzar desempeño máximo |
|---|---|---|---|
| [x] | IE1/IE4: audiencia identificada | Directorio, Contenidos y Marketing definidos | Relacionar cada KPI con una decisión concreta en la presentación |
| [x] | IE2: propósito comunicacional | Apoyar adquisición, marketing y producto | Escribir una frase de propósito medible para EP1 |
| [x] | IE3: estrategia de comunicación | Storytelling, limitaciones y guion ejecutivo documentados | Aplicar el guion en la presentación |
| [x] | IE8: fundamento técnico visual | Justificación de barras, ranking, líneas y dispersión | Añadir escala, orden, color y accesibilidad de cada visual |
| [~] | IE11: integración oral, escrita y visual | Notebook, informe, figuras y guion existen | Crear/exportar la presentación y ensayar |
| [x] | IE12: conclusiones basadas en evidencia | Hallazgos incluyen cifras y limitaciones | Asociar cada recomendación a KPI, tabla y visual específico |
| [x] | Claridad de títulos y etiquetas | Títulos, ejes y leyendas en figuras | Revisar legibilidad en tamaño de presentación y móvil |
| [~] | Accesibilidad visual | Paleta contrastante, texto y ejes explícitos | Comprobar contraste y tamaño en revisión final |
| [x] | Reproducibilidad completa | `requirements.txt`, notebook y documentación | Probar instalación en entorno limpio |
| [~] | Dashboard funcional | `dashboard/app.py` con filtros, tooltips y descarga; sintaxis validada | Instalar desde `requirements.txt` en el intérprete activo y revisar visualmente |
| [ ] | Prueba de usabilidad | Protocolo listo, sin participantes registrados | Ejecutar con las tres audiencias y documentar resultados |
| [~] | Evaluación crítica EP3 | Informe de riesgos y mejoras iniciales | Registrar resultados de la prueba antes/después |
| [~] | Presentación ejecutiva PDF/PPT | Guion completo, aún sin archivo de diapositivas | Crear y exportar la presentación |
| [~] | Informe ejecutivo PDF | MD con resultados y limitaciones | Exportar PDF y revisar formato final |
| [~] | Defensa individual | Guion y preguntas preparados | Ensayar y registrar roles |

## 4. Criterio de cierre

### Para considerar cerrado el EDA (EP1)

- [x] Incorporar tablas por tipo para popularidad, géneros y países.
- [x] Añadir fórmulas, unidades y cobertura de cada KPI.
- [x] Completar auditoría de rangos, nulos por columna y valores extremos.
- [ ] Revisar accesibilidad de las cinco figuras.
- [ ] Actualizar `EP1_informe_ejecutivo.md` con cifras, visuales y recomendaciones.
- [ ] Exportar y revisar el PDF de EP1.

### Para considerar cerrado el proyecto completo

- [~] Implementar el dashboard según `dashboard_visual_plan.csv`.
- [x] Añadir filtros, navegación, tooltips y exportación.
- [ ] Probar el dashboard con Directorio, Contenidos y Marketing.
- [ ] Documentar mejoras de EP3.
- [ ] Preparar presentación y defensa individual.
- [ ] Verificar ejecución desde un entorno limpio.

## Veredicto actual

**Resultado:** el EDA cumple de forma sólida los análisis centrales del caso y se reforzó con auditorías, fórmulas, accesibilidad, tablas por tipo y un dashboard implementado estáticamente. Aún no puede declararse 100% cerrado porque el dashboard necesita validación de ejecución en el entorno activo, y las pruebas con usuarios, PDF, presentación final y defensa requieren ejecución humana.

La siguiente prioridad recomendada es cerrar EP1: reforzar la evidencia técnica, actualizar el informe ejecutivo y preparar el diseño funcional del dashboard antes de programarlo.
