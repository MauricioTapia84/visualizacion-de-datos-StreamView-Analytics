# Checklist maestro del proyecto StreamView Analytics

## Estado actual del proyecto vs. enfoque final propuesto

### Lo que ya existe en el proyecto actual

- [X] Base de trabajo funcional en notebooks y datasets procesados.
- [X] EDA y limpieza con análisis descriptivo del catálogo.
- [X] Separación train/test y export de datasets procesados.
- [X] Notebook de modelado con validación supervisada.
- [X] Clustering no supervisado con gráficos del codo y resumen por clusters.
- [X] Export de artefactos de modelo en `models/`.
- [X] Archivo HTML de mockup de baja fidelidad en `docs/mockup_dashboard_baja_fidelidad.html`.
- [X] Estructura base del dashboard y carpetas de datos/artefactos lista para consumos BI.

### Lo que aún falta para dejarlo alineado con la visión final

- [ ] Definir formalmente `indice_exito` continuo con ponderación de popularity, vote_count y vote_average.
- [ ] Derivar categorías `Bajo Éxito`, `Medio Éxito`, `Alto Éxito`.
- [ ] Ajustar la lógica del target para que no dependa solo de `type` ni de una clasificación inmediata arbitraria.
- [ ] Dejar la validación final exclusivamente en test para evitar leakage.
- [X] Preparar la guía de DataStudio con estructura de dashboard y mockup asociado.
- [X] Generar CSVs separados y optimizados por uso: ejecutivo, contenidos y predicciones.
- [ ] Documentar la justificación de codificación categórica y escalado numérico con evidencia gráfica.
- [ ] Añadir evaluación de SHAP y métricas de negocio más alineadas a la decisión.
- [ ] Validar el uso de `budget` y `revenue` como señales de costo-beneficio para películas.

---

## Checklist maestro de trabajo

### 1. Alcance y arquitectura del proyecto

- [X] Mantener la capa descriptiva del catálogo.
- [X] Añadir una capa predictiva orientada a decisiones de adquisición y producción.
- [X] Mantener la idea de dashboard descriptivo + dashboard predictivo.
- [X] Definir claramente la arquitectura de entregable final: notebooks, pipeline, CSVs y artefactos del modelo.
- [X] Mantener la lógica de trabajo por fases: EDA, modelado, validación y dashboard.
- [X] Aceptar que el modelo complementa, no reemplaza, la narrativa analítica.

### 2. Definición del target y de la decisión de negocio

- [ ] Definir `indice_exito` como variable continua en escala 0 a 1.
- [ ] Normalizar `popularity`, `vote_count` y `vote_average` con Min-Max o equivalente.
- [ ] Ponderar la combinación con pesos sugeridos: 40% popularity, 30% vote_count, 30% vote_average.
- [ ] Crear la clasificación derivada `alto_exito`, `medio_exito`, `bajo_exito`.
- [ ] Elegir umbral sugerido de negocio: `indice_exito >= 0.60` = Alto, etc.
- [ ] Validar y ajustar los cortes con distribución empírica real.
- [ ] Justificar que `vote_count` y `vote_average` se deben analizar juntos.
- [ ] Incorporar `budget` y `revenue` como indicadores de costo-beneficio solo para películas.
- [ ] Explícitamente advertir que `popularity` es un índice relativo de la fuente y no consumo real de StreamView.

### 3. Calidad de datos y prevención de leakage

- [X] Revisar estructura de datos, tipos y nulos.
- [X] Validar duplicados y columnas irrelevantes.
- [X] Realizar split 80/20 antes de transformaciones.
- [ ] Dejar documentado el flujo exacto: split -> preprocessing -> modelo -> evaluación.
- [X] Mantener los CSVs procesados como base reproducible.
- [ ] Asegurar que el modelo final se evalúa exclusivamente en test.
- [ ] Justificar con evidencia que no hubo leakage en ingeniería de features ni codificación.

### 4. EDA y validación analítica

- [X] Revisar inspección inicial con `df.info()`.
- [X] Revisar distribuciones numéricas y sesgos.
- [ ] Revisar distribuciones con evidencia gráfica para justificar scaling.
- [X] Revisar variables categóricas y su cardinalidad.
- [X] Revisar correlación entre variables relevantes.
- [ ] Evaluar la relación `vote_count` vs `vote_average` con scatter plot y correlación.
- [ ] Hacer análisis por tipo (`Movie` vs `TV Show`) cuando la relación cambie por formato.
- [ ] Incluir conclusiones por sección con cierre formal del EDA.

### 5. Feature engineering

- [ ] Definir claramente la etapa de `02_Feature_Engineering.ipynb`.
- [ ] Crear `indice_exito` como target continuo.
- [ ] Generar categorías de éxito mediante umbral de negocio.
- [ ] Decidir transformaciones numéricas (log, scaling, clipping).
- [ ] Revisar varianza cero, correlación y redundancia.
- [ ] Definir codificación para variables categóricas.
- [ ] Agregar features útiles para el dashboard y la recomendación de adquisición.
- [ ] Guardar versions limpias de train/test listas para modelado.
- [ ] Exportar CSVs para dashboard en formatos optimizados.

### 6. Modelado no supervisado

- [X] Ejecutar clustering con KMeans.
- [X] Revisar gráfico del codo.
- [X] Revisar resumen de clusters por métricas clave.
- [ ] Incluir PCA para mostrar separación visual de clusters.
- [ ] Correlacionar clusters con `indice_exito` o con variables de valor.
- [ ] Añadir conclusión analítica del clustering para uso del dashboard.

### 7. Modelos supervisados y tuning

- [X] Comparar modelos base y evaluar rendimiento.
- [X] Mantener validación con RandomForest y modelo entrenado de base.
- [ ] Comparar al menos 3 modelos: regresión lineal, random forest y XGBoost.
- [ ] Debatir si XGBoost es la mejor opción para el caso.
- [ ] Evaluar Optuna como búsqueda de hiperparámetros.
- [ ] Definir métrica prioritaria del problema de negocio.
- [ ] Usar métricas de clasificación y regresión en una misma evaluación.
- [ ] Dar prioridad a indicadores de decisión real, no solo accuracy.

### 8. Métricas y criterio de negocio

- [ ] Definir prioridad de métricas por contexto del problema.
- [ ] Para la predicción continua: RMSE/MAE.
- [ ] Para clasificación binaria: F1, Precision, Recall, ROC-AUC, PR-AUC.
- [ ] Para ranking de recomendación: Precision@K o top-N.
- [ ] Usar ganancia acumulada y lift como apoyo de negocio para priorizar títulos.
- [ ] Justificar por qué el modelo sirve para decidir adquisición y producción, no solo para describir tendencias.

### 9. Interpretabilidad y explicabilidad

- [ ] Añadir SHAP a la validación final.
- [ ] Mostrar qué variables influyen más en el éxito.
- [ ] Explicar en texto la relación entre variables y decisión de negocio.
- [ ] Vincular SHAP con dashboard de adquisición recomendado.

### 10. Dashboard y DataStudio

- [X] Existe mockup HTML de baja fidelidad con Bootstrap.
- [ ] Alinear el mockup con el diseño actual del PDF señalado.
- [X] Definir la guía de dashboard en DataStudio.
- [X] Separar panel descriptivo y panel predictivo.
- [X] Incorporar métricas de `vote_average`, `vote_count`, `type`, `budget`, `revenue`.
- [X] Diseñar filtros por tipo, género, país, idioma, año y nivel de éxito.
- [X] Diseñar KPIs ejecutivos de referencia.
- [X] Diseñar panel de ranking por `indice_exito`.
- [X] Diseñar scatter plot `vote_count` vs `vote_average`.
- [X] Diseñar scatter plot `budget` vs `revenue` para películas.
- [X] Añadir tablas de recomendación de adquisición con prioridad.
- [X] Documentar la estructura final de entregable para DataStudio.

### 11. CSVs para dashboard y pipeline

- [X] Existen al menos datasets procesados y artefactos funcionales.
- [X] Crear `csv_dashboard_ejecutivo.csv` optimizado para KPIs.
- [X] Crear `csv_dashboard_contenidos.csv` optimizado para análisis por género, país y tipo.
- [X] Crear `csv_dashboard_predicciones.csv` con predicciones, score y clase.
- [X] Guardar cada CSV con columnas relevantes y sin sobrecarga innecesaria.
- [X] Separar claramente el uso del modelo del uso del dashboard descriptivo.

### 12. Pipeline y reproducibilidad

- [X] Crear `pipeline.py` final con todo el flujo reproducible.
- [X] Guardar artefactos del modelo (`.pkl`/`.joblib`).
- [X] Documentar ejecución del pipeline.
- [ ] Dejar reproducibilidad y orden de ejecución de notebooks.
- [ ] Validar que la ejecución final produzca resultados reales en entorno limpio.

### 13. Revisión adicional con PyCaret

- [X] Se acepta la validación adicional con PyCaret como comparación y benchmark.
- [ ] Definir si PyCaret será solo un benchmark adicional o una ruta complementaria.
- [ ] No usar PyCaret como reemplazo del flujo principal de sklearn.
- [ ] Documentar la comparación y la conclusión.

---

## Estado de cumplimiento actual (11/11/2026)

### Completado

- [X] Base funcional del proyecto y estructura principal
- [X] Revisión de calidad y limpieza inicial
- [X] Separación train/test base
- [X] Clustering y visualizaciones no supervisadas
- [X] Modelado supervisado funcional y validado
- [X] Export de artefactos del modelo
- [X] Mockup HTML base en Bootstrap
- [X] Guía preliminar de dashboard en docs

### Pendiente crítico

- [ ] Implementar target `indice_exito` formal
- [ ] Crear tres niveles de éxito (`bajo/medio/alto`)
- [ ] Completar pipeline reproducible final
- [X] Generar CSVs separados para Dashboard/DataStudio
- [X] Reforzar la guía de DataStudio con estructura final y mockup y componentes visuales reales
- [ ] Incorporar SHAP y métricas de negocio más orientadas a decisión

---

## Conclusión práctica

El proyecto actual ya está bien encaminado como base analítica y predictiva, pero para cumplir completamente con la propuesta final debe pasar por una consolidación de target, pipeline y dashboard BI. La clave está en dejar la parte descriptiva y la predictiva separadas, pero conectadas: el dashboard final debe responder dos preguntas simultáneas:

1. ¿Qué está pasando en el catálogo? (descriptivo)
2. ¿Qué títulos deberían priorizarse para adquisición o producción? (predictivo)

Esto es lo que hace que el proyecto no sea solo un análisis de datos, sino una herramienta de decisión real.
