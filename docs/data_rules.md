
# StreamView Analytics - Data Rules

## 1. Fuentes originales

Los archivos ubicados en `data/raw/` son las fuentes oficiales.

Nunca deben:

- sobrescribirse;
- modificarse directamente;
- reemplazarse.

Todas las transformaciones deben generar nuevos archivos.

---

## 2. Integración

Movies y TV Shows representan contenidos distintos.

Por lo tanto, deben integrarse mediante concatenación vertical
(union / concat), NO mediante JOIN o MERGE entre registros.

El resultado debe mantener:

1 contenido audiovisual = 1 fila.

---

## 3. Tipo de contenido

Debe ser posible distinguir entre:

- Movie
- TV Show

La variable `type` debe conservar o permitir esta identificación
en el dataset integrado.

---

## 4. Variables comunes

Las columnas equivalentes entre Movies y TV Shows deben tener:

- nombres compatibles;
- tipos de datos compatibles;
- significado equivalente.

No cambiar el significado original de las variables.

---

## 5. Variables exclusivas de películas

Las variables:

- budget
- revenue

corresponden exclusivamente a películas.

En registros de TV Shows deben permanecer como valores no disponibles
(NULL / NaN) si forman parte del esquema integrado.

Nunca reemplazarlas por 0.

---

## 6. Popularity

`popularity` representa un índice relativo de popularidad.

No debe interpretarse ni renombrarse como:

- reproducciones;
- visualizaciones;
- consumo;
- cantidad de usuarios.

---

## 7. Valores faltantes

No imputar valores faltantes de forma automática.

Los valores faltantes deben conservarse cuando:

- representen información no disponible;
- la variable no sea aplicable;
- no exista una regla justificable para reemplazarlos.

Los textos vacíos pueden normalizarse a valores nulos cuando corresponda.

---

## 8. Duplicados

Detectar registros duplicados antes de eliminarlos.

Se pueden eliminar filas completamente duplicadas cuando la duplicidad
sea verificable.

Si existen identificadores repetidos con información diferente,
NO resolverlos automáticamente.

Debe informarse el caso antes de modificar los datos.

---

## 9. Limpieza de texto

Se permite corregir problemas puramente estructurales como:

- espacios iniciales o finales;
- cadenas vacías;
- diferencias de formato claramente equivalentes.

No cambiar categorías o valores basándose únicamente en suposiciones.

---

## 10. Granularidad

No dividir `genres`, `country`, `language`, `cast` u otras variables
multivalor en múltiples filas durante esta etapa.

El dataset maestro debe conservar una fila por contenido.

---

## 11. Resultado

El dataset final debe guardarse en:

data/processed/catalogo_streamview.csv

Los archivos originales deben permanecer intactos.
