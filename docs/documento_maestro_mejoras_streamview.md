# Documento Maestro de Mejoras - Proyecto StreamView Analytics (Etapa 3)

## 1. Objetivo

Este documento consolida las correcciones, observaciones y aprendizajes obtenidos a partir de la retroalimentación del docente y de las guías de evaluación del dashboard, el problema de negocio y la propuesta conceptual. Su propósito es dejar una base sólida para la etapa final del proyecto, con foco en decisión de negocio, rigor analítico y producción del material de defensa.

## 2. Resumen ejecutivo de correcciones

| Área | Corrección | Prioridad |
|---|---|---|
| Problema de negocio | Enfocarse en factores de éxito para adquisición, renovación y producción, no en la mera comunicación del catálogo | Alta |
| Decisión | Reformular la decisión como qué adquirir, renovar o producir para maximizar popularidad y valoración | Alta |
| Audiencias | Justificar por qué el Gerente de Contenidos y Adquisición es el stakeholder principal | Alta |
| Variables | Incluir y justificar variables como type, release_year, date_added, vote_count y budget/revenue | Alta |
| Árbol de preguntas | La raíz debe ser la decisión de negocio y no la composición del catálogo | Alta |
| Reglas de negocio | Fijar mínimo de vote_count y advertir la naturaleza relativa de popularity | Media |
| Dashboard | Incorporar vote_average, vote_count, type, budget, revenue y métricas comparativas | Alta |
| Terminología | Reemplazar “multicolinealidad” por “redundancia” | Media |
| Rigor analítico | Usar cifras reales del conjunto analizado y evitar supuestos inexistentes | Media |
| Variable compuesta | Incorporar indice_exito como indicador de éxito consolidado | Media |

## 3. Correcciones del problema de negocio y la decisión

### Problema de negocio corregido

Netflix necesita identificar qué factores del contenido —género, país, idioma, presupuesto y tipo de título— se asocian con mayores niveles de popularidad y valoración de los usuarios, para orientar decisiones de adquisición, renovación y producción de nuevo contenido. Actualmente, la dirección de contenidos no cuenta con un análisis consolidado que permita distinguir qué características del catálogo explican mejor el éxito de un título, lo que dificulta priorizar inversiones y definir la composición futura del catálogo.

### Decisión a tomar corregida

Definir qué géneros, países, idiomas y contenidos conviene priorizar en las próximas decisiones de adquisición, renovación y producción del catálogo, con el fin de maximizar la popularidad y valoración de los títulos incorporados.

## 4. Ajuste de audiencias y stakeholders

El usuario principal debe ser el Gerente de Contenidos y Adquisición. Su decisión requiere evaluar detalladamente géneros, países, idiomas y títulos, mientras que el Directorio funciona como audiencia secundaria del resumen ejecutivo.

## 5. Variables y datos

Se seleccionan las siguientes variables prioritarias:

- popularity: métrica principal de éxito relativo; debe mostrarse con advertencia de que no mide reproducciones reales.
- vote_average: mide la valoración percibida por el usuario.
- vote_count: contextualiza la valoración y evita interpretaciones con poca evidencia.
- genres: identifica categorías temáticas con mayor potencial.
- country: revela mercados con mejor desempeño.
- language: complementa el análisis geográfico y cultural.
- type: diferencia series de películas.
- release_year / date_added: permiten analizar evolución temporal.
- budget y revenue: solo aplicables a películas con cobertura parcial.

## 6. Árbol de preguntas corregido

### Raíz de decisión

¿Qué géneros, países y contenidos priorizar en las próximas adquisiciones y renovaciones?

### Rama 1: Composición del catálogo

- ¿Cómo se distribuye el catálogo entre películas y series?
- Variables: type, release_year, date_added

### Rama 2: Géneros con mayor presencia y éxito

- ¿Qué géneros concentran más títulos?
- ¿Qué géneros presentan mayor popularidad relativa?
- Variables: genres, popularity

### Rama 3: Relación entre popularidad y valoración

- ¿Los géneros más populares también son los mejor valorados?
- ¿Existe suficiente respaldo de evaluaciones?
- Variables: popularity, vote_average, vote_count

### Rama 4: Mercados y idiomas

- ¿Qué países e idiomas lideran en popularidad y valoración?
- Variables: country, language, genres, popularity, vote_average

### Rama 5: Títulos candidatos

- ¿Qué títulos presentan señales más relevantes para adquisición, renovación o promoción?
- Variables: title, type, genres, country, popularity, vote_average, vote_count

## 7. Reglas de negocio

### Regla 1: mínimo de voto

Para el análisis de valoración, se aplica un mínimo de 100 evaluaciones, con la regla vote_count >= 100. Esto evita interpretar como sólido un rating construido sobre pocas valoraciones.

### Regla 2: popularity como índice relativo

La variable popularity es un índice relativo calculado por la fuente; no representa reproducciones reales ni usuarios de StreamView. Además, no es directamente comparable entre películas y series, por lo que debe usarse con advertencia visible en todo el dashboard.

## 8. Mejoras propuestas al dashboard

1. Incorporar vote_average y vote_count en todas las visualizaciones relevantes.
2. Distinguir películas y series con filtros globales y comparativas separadas.
3. Reemplazar un KPI único por un panel comparativo de KPIs ejecutivos.
4. Añadir un scatter plot de popularity vs vote_average con filtro vote_count >= 100.
5. Incluir análisis financiero con ROI para películas con datos válidos.
6. Reemplazar mapas de conteos por mapas de desempeño promedio por país.
7. Incluir indice_exito como columna clave en la tabla de títulos potenciales.

## 9. Information scent y progressive disclosure

Se mantiene el enfoque de navegación progresiva:

- Nivel 1: KPIs ejecutivos
- Nivel 2: diferenciación por género, país e idioma
- Nivel 3: detalle de títulos y priorización
- Nivel 4: tabla de decisiones con contexto y advertencias

## 10. Terminología y rigor

Se reemplaza la expresión “multicolinealidad” por “redundancia” cuando se habla de variables relacionadas. También se debe evitar usar cifras que no correspondan al modelo real y se debe mantener una atención constante a los límites de calidad de los datos.

## 11. Propuesta de variable compuesta: indice_exito

La variable compuesta indice_exito combina popularidad y respaldo de votos para identificar contenidos con éxito consolidado y no solo visibilidad aislada. El objetivo es distinguir entre un título viral de corto alcance y un contenido con sólida base de apoyo y percepción positiva.

## 12. Checklist maestro de mejoras

### Informe

- [ ] Reescribir el problema de negocio con foco en factores de éxito
- [ ] Reformular la decisión como adquisición, renovación y producción
- [ ] Justificar al stakeholder principal
- [ ] Incluir tabla de variables con justificación individual
- [ ] Rehacer árbol de preguntas con raíz de negocio
- [ ] Fijar regla de vote_count mínimo
- [ ] Advertir la naturaleza relativa de popularity
- [ ] Reemplazar “multicolinealidad” por “redundancia”
- [ ] Incorporar indice_exito
- [ ] Incluir estructura de carpetas y README del proyecto

### Dashboard

- [ ] Incorporar vote_average y vote_count
- [ ] Añadir filtro por type
- [ ] Crear panel comparativo de KPIs
- [ ] Incluir scatter popularity vs vote_average
- [ ] Añadir análisis financiero para películas
- [ ] Mostrar advertencias de negocio
- [ ] Incorporar indice_exito en la tabla de recomendación

### Presentación

- [ ] Preparar guion por expositor
- [ ] Practicar transiciones entre secciones
- [ ] Preparar respuestas a preguntas cruzadas
- [ ] Verificar dominio completo del proyecto

## 13. Mensaje recomendado para el informe Fase 3

La propuesta de mejora del dashboard y del informe de fase 3 se fundamenta en un cambio importante de enfoque: la decisión de negocio ya no es “describir el catálogo”, sino “identificar qué factores explican el éxito del contenido y qué títulos conviene priorizar para adquisición, renovación o producción”. Este ajuste mejora la alineación con el objetivo del caso y permite que el análisis deje de ser descriptivo para volverse accionable y estratégico.

## 14. Mensaje recomendado para la defensa / PPT 3

El valor del proyecto no radica en mostrar más gráficos, sino en tomar decisiones con mejor fundamento. StreamView Analytics combina análisis descriptivo y priorización estratégica para convertir el catálogo en una herramienta de decisión para la adquisición, renovación y producción de contenidos.
