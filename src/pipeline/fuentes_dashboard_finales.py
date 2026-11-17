"""Genera la capa de datos final para Looker Studio.

Este pipeline parte directamente de los CSV originales, conserva la granularidad
de una fila por contenido en la fuente principal y genera tablas puente para los
campos multivaluados de géneros y países.

No usa el catálogo procesado ni los artefactos predictivos existentes.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
DASHBOARD_DIR = ROOT / "data" / "dashboard"

MOVIES_FILE = RAW_DIR / "netflix_movies_detailed_up_to_2025.csv"
TV_FILE = RAW_DIR / "netflix_tv_shows_detailed_up_to_2025.csv"

CONTENT_FILE = DASHBOARD_DIR / "dashboard_contenidos_final.csv"
GENRES_FILE = DASHBOARD_DIR / "dashboard_generos.csv"
COUNTRIES_FILE = DASHBOARD_DIR / "dashboard_paises.csv"
VALIDATION_JSON = DASHBOARD_DIR / "dashboard_validation.json"
VALIDATION_MD = DASHBOARD_DIR / "dashboard_validation.md"
README_FINAL = DASHBOARD_DIR / "README_fuentes_finales.md"

CONTENT_FIELDS = [
    "id_contenido",
    "titulo",
    "tipo",
    "generos",
    "pais",
    "idioma",
    "anio_publicacion",
    "popularidad",
    "votos",
    "valoracion_promedio",
    "presupuesto",
    "ingresos",
]

GENRE_FIELDS = [
    "id_contenido",
    "genero_individual",
    "tipo",
    "popularidad",
    "votos",
    "valoracion_promedio",
    "anio_publicacion",
    "idioma",
    "pais",
]

COUNTRY_FIELDS = [
    "id_contenido",
    "pais_individual",
    "tipo",
    "popularidad",
    "votos",
    "valoracion_promedio",
    "anio_publicacion",
    "idioma",
    "generos",
]

NULL_MARKERS = {"", "nan", "none", "null"}
FINANCIAL_FIELDS = {"budget", "revenue"}


def is_null(value: Any) -> bool:
    return value is None or str(value).strip().lower() in NULL_MARKERS


def clean_text(value: Any) -> str | None:
    if is_null(value):
        return None
    cleaned = str(value).strip()
    return cleaned or None


def parse_decimal(value: Any) -> Decimal | None:
    if is_null(value):
        return None
    try:
        return Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        return None


def format_numeric(value: Any, *, integer: bool = False) -> str | None:
    number = parse_decimal(value)
    if number is None:
        return None
    if integer:
        if number != number.to_integral_value():
            return format(number.normalize(), "f")
        return str(int(number))
    return format(number.normalize(), "f")


def format_financial(value: Any) -> str | None:
    number = parse_decimal(value)
    if number is None or number == 0:
        return None
    return format(number.normalize(), "f")


def source_hash(row: dict[str, str]) -> str:
    payload = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def type_prefix(content_type: str) -> str:
    if content_type == "Movie":
        return "Movie"
    if content_type == "TV Show":
        return "TV"
    normalized = re.sub(r"[^A-Za-z0-9]+", "_", content_type).strip("_")
    return normalized or "Content"


def read_source(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"La fuente no tiene encabezado: {path}")
        if "show_id" not in reader.fieldnames or "type" not in reader.fieldnames:
            raise ValueError(f"La fuente no contiene show_id y type: {path}")
        return [dict(row) for row in reader]


def assign_stable_ids(rows: list[dict[str, str]]) -> dict[str, Any]:
    base_ids: list[str] = []
    hashes: list[str] = []
    for row in rows:
        content_type = clean_text(row.get("type")) or "Content"
        show_id = clean_text(row.get("show_id"))
        digest = source_hash(row)
        hashes.append(digest)
        base_ids.append(f"{type_prefix(content_type)}_{show_id}" if show_id else "")

    base_counts = Counter(base_ids)
    stable_ids: list[str] = []
    for base_id, digest in zip(base_ids, hashes):
        if not base_id:
            stable_ids.append(f"MissingId_{digest}")
        elif base_counts[base_id] == 1:
            stable_ids.append(base_id)
        else:
            stable_ids.append(f"{base_id}_{digest[:16]}")

    return {
        "ids": stable_ids,
        "base_id_counts": base_counts,
        "missing_show_id_count": sum(not value for value in base_ids),
        "same_type_duplicate_base_ids": sum(count > 1 for count in base_counts.values()),
    }


def build_records(raw_rows: list[dict[str, str]], stable_ids: list[str]) -> list[dict[str, str | None]]:
    records: list[dict[str, str | None]] = []
    for row, stable_id in zip(raw_rows, stable_ids):
        records.append(
            {
                "id_contenido": stable_id,
                "titulo": clean_text(row.get("title")),
                "tipo": clean_text(row.get("type")),
                "generos": clean_text(row.get("genres")),
                "pais": clean_text(row.get("country")),
                "idioma": clean_text(row.get("language")),
                "anio_publicacion": format_numeric(row.get("release_year"), integer=True),
                "popularidad": format_numeric(row.get("popularity")),
                "votos": format_numeric(row.get("vote_count"), integer=True),
                "valoracion_promedio": format_numeric(row.get("vote_average")),
                "presupuesto": format_financial(row.get("budget")),
                "ingresos": format_financial(row.get("revenue")),
            }
        )
    return records


def split_multivalue(value: str | None) -> list[str]:
    if is_null(value):
        return []
    result: list[str] = []
    seen: set[str] = set()
    for item in str(value).split(","):
        cleaned = item.strip()
        if cleaned and cleaned not in seen:
            result.append(cleaned)
            seen.add(cleaned)
    return result


def build_relation_rows(
    records: list[dict[str, str | None]],
    source_field: str,
    relation_field: str,
    extra_fields: list[tuple[str, str]],
) -> list[dict[str, str | None]]:
    rows: list[dict[str, str | None]] = []
    seen: set[tuple[str, str]] = set()
    for record in records:
        content_id = str(record["id_contenido"])
        for value in split_multivalue(record.get(source_field)):
            relation_key = (content_id, value)
            if relation_key in seen:
                continue
            seen.add(relation_key)
            relation = {
                "id_contenido": content_id,
                relation_field: value,
            }
            for output_field, source_key in extra_fields:
                relation[output_field] = record.get(source_key)
            rows.append(relation)
    return sorted(rows, key=lambda row: (str(row["id_contenido"]), str(row[relation_field])))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str | None]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: "" if row.get(field) is None else row.get(field) for field in fields})


def count_nulls(rows: list[dict[str, Any]], fields: list[str]) -> dict[str, int]:
    return {field: sum(is_null(row.get(field)) for row in rows) for field in fields}


def output_summary(rows: list[dict[str, Any]], fields: list[str], relation_field: str | None = None) -> dict[str, Any]:
    ids = [str(row.get("id_contenido")) for row in rows]
    id_counts = Counter(ids)
    relation_duplicates = 0
    if relation_field:
        relations = [(str(row.get("id_contenido")), str(row.get(relation_field))) for row in rows]
        relation_duplicates = len(relations) - len(set(relations))
    return {
        "rows": len(rows),
        "columns": len(fields),
        "field_names": fields,
        "unique_id_contenido": len(set(ids)),
        "duplicate_id_contenido": sum(count - 1 for count in id_counts.values() if count > 1),
        "duplicate_relation_rows": relation_duplicates,
        "nulls_by_field": count_nulls(rows, fields),
        "unique_relation_values": len({str(row[relation_field]) for row in rows if not is_null(row.get(relation_field))}) if relation_field else None,
    }


def top_distinct(records: list[dict[str, str | None]], field: str) -> list[dict[str, Any]]:
    ids_by_value: defaultdict[str, set[str]] = defaultdict(set)
    for record in records:
        content_id = str(record["id_contenido"])
        for value in split_multivalue(record.get(field)):
            ids_by_value[value].add(content_id)
    ranked = sorted(ids_by_value.items(), key=lambda item: (-len(item[1]), item[0]))[:10]
    return [{"valor": value, "count_distinct_id_contenido": len(ids)} for value, ids in ranked]


def financial_summary(records: list[dict[str, str | None]], raw_rows: list[dict[str, str]]) -> dict[str, Any]:
    movies = [record for record in records if record["tipo"] == "Movie"]
    tv_shows = [record for record in records if record["tipo"] == "TV Show"]
    source_zero_counts = {
        field: sum(parse_decimal(row.get(field)) == 0 for row in raw_rows if not is_null(row.get(field)))
        for field in FINANCIAL_FIELDS
    }
    final_zero_counts = {
        field: sum(parse_decimal(record.get(output)) == 0 for record in records if not is_null(record.get(output)))
        for field, output in [("budget", "presupuesto"), ("revenue", "ingresos")]
    }

    movie_budget = sum(not is_null(record["presupuesto"]) for record in movies)
    movie_revenue = sum(not is_null(record["ingresos"]) for record in movies)
    movie_both = sum(not is_null(record["presupuesto"]) and not is_null(record["ingresos"]) for record in movies)
    movie_total = len(movies)

    return {
        "movies_total": movie_total,
        "tv_shows_total": len(tv_shows),
        "movies_with_budget": movie_budget,
        "movies_with_revenue": movie_revenue,
        "movies_with_both_financial_fields": movie_both,
        "movie_financial_coverage_percent": round(movie_both / movie_total * 100, 4) if movie_total else 0.0,
        "tv_shows_with_valid_budget": sum(not is_null(record["presupuesto"]) for record in tv_shows),
        "tv_shows_with_valid_revenue": sum(not is_null(record["ingresos"]) for record in tv_shows),
        "source_zero_counts_converted_to_null": source_zero_counts,
        "final_zero_counts": final_zero_counts,
    }


def build_validation(
    raw_rows: list[dict[str, str]],
    records: list[dict[str, str | None]],
    genre_rows: list[dict[str, str | None]],
    country_rows: list[dict[str, str | None]],
    id_info: dict[str, Any],
) -> dict[str, Any]:
    all_show_ids = [clean_text(row.get("show_id")) for row in raw_rows]
    show_id_counts = Counter(value for value in all_show_ids if value is not None)
    types_by_show_id: defaultdict[str, set[str]] = defaultdict(set)
    for row in raw_rows:
        show_id = clean_text(row.get("show_id"))
        if show_id:
            types_by_show_id[show_id].add(clean_text(row.get("type")) or "")

    content_summary = output_summary(records, CONTENT_FIELDS)
    genre_summary = output_summary(genre_rows, GENRE_FIELDS, "genero_individual")
    country_summary = output_summary(country_rows, COUNTRY_FIELDS, "pais_individual")
    finance = financial_summary(records, raw_rows)

    checks = {
        "source_has_32000_rows": len(raw_rows) == 32000,
        "source_has_16000_movies": sum(row.get("type") == "Movie" for row in raw_rows) == 16000,
        "source_has_16000_tv_shows": sum(row.get("type") == "TV Show" for row in raw_rows) == 16000,
        "content_has_exactly_32000_rows": content_summary["rows"] == 32000,
        "content_has_one_row_per_content": content_summary["rows"] == content_summary["unique_id_contenido"],
        "content_has_no_duplicate_ids": content_summary["duplicate_id_contenido"] == 0,
        "content_has_required_columns_only": content_summary["field_names"] == CONTENT_FIELDS,
        "content_has_no_predictive_columns": not any(field.startswith("pred_") or field in {"indice_exito", "categoria_exito"} for field in content_summary["field_names"]),
        "genre_relations_have_no_duplicates": genre_summary["duplicate_relation_rows"] == 0,
        "country_relations_have_no_duplicates": country_summary["duplicate_relation_rows"] == 0,
        "tv_shows_have_no_valid_budget": finance["tv_shows_with_valid_budget"] == 0,
        "tv_shows_have_no_valid_revenue": finance["tv_shows_with_valid_revenue"] == 0,
        "financial_zeros_are_not_exported_as_zero": all(value == 0 for value in finance["final_zero_counts"].values()),
        "all_source_rows_have_show_id": id_info["missing_show_id_count"] == 0,
        "all_output_ids_are_unique": content_summary["duplicate_id_contenido"] == 0,
    }

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "sources": {
            "movies": str(MOVIES_FILE.relative_to(ROOT)),
            "tv_shows": str(TV_FILE.relative_to(ROOT)),
            "combined_rows": len(raw_rows),
            "combined_unique_show_id": len(show_id_counts),
            "combined_duplicate_show_id_rows": sum(count - 1 for count in show_id_counts.values() if count > 1),
            "combined_duplicate_show_id_values": sum(count > 1 for count in show_id_counts.values()),
            "cross_type_show_id_collisions": sum(len(types) > 1 for types in types_by_show_id.values()),
        },
        "id_strategy": {
            "base": "type_prefix + show_id",
            "same_type_collision_resolution": "append deterministic SHA-256 fragment of the complete source row",
            "same_type_duplicate_base_id_values": id_info["same_type_duplicate_base_ids"],
            "missing_show_id_count": id_info["missing_show_id_count"],
            "stable_id_unique_count": len({record["id_contenido"] for record in records}),
        },
        "outputs": {
            "dashboard_contenidos_final.csv": content_summary,
            "dashboard_generos.csv": genre_summary,
            "dashboard_paises.csv": country_summary,
        },
        "financial": finance,
        "top_10_generos": top_distinct(records, "generos"),
        "top_10_paises": top_distinct(records, "pais"),
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "predictive_scope": {
            "modeling_exports_in_content_source": False,
            "note": "Las predicciones experimentales existentes no se incluyen en esta capa. El pipeline predictivo actual predice las 32000 filas completas, mezclando filas usadas en entrenamiento y prueba; además, indice_exito se construye con variables que también se entregan al modelo.",
        },
    }


def write_validation_markdown(report: dict[str, Any]) -> None:
    outputs = report["outputs"]
    financial = report["financial"]
    checks = report["checks"]
    lines = [
        "# Validación de fuentes finales para Looker Studio",
        "",
        f"Estado: **{report['status']}**",
        "",
        "## Salidas",
        "",
        "| Archivo | Filas | Columnas | IDs únicos | Duplicados de ID | Nulos por campo |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for filename, summary in outputs.items():
        lines.append(
            f"| `{filename}` | {summary['rows']} | {summary['columns']} | {summary['unique_id_contenido']} | {summary['duplicate_id_contenido']} | `{summary['nulls_by_field']}` |"
        )
    lines.extend(
        [
            "",
            "## Identificador",
            "",
            f"`show_id` combinado único: **{report['sources']['combined_unique_show_id']}** de {report['sources']['combined_rows']} filas.",
            f"Colisiones entre tipos: **{report['sources']['cross_type_show_id_collisions']}**.",
            f"Valores base duplicados dentro de un mismo tipo: **{report['id_strategy']['same_type_duplicate_base_id_values']}**.",
            "",
            "Los IDs normales usan `Movie_<show_id>` o `TV_<show_id>`. Cuando el par tipo/show_id se repite, se añade un fragmento determinista de SHA-256 de la fila original; no se usa el orden de las filas.",
            "",
            "## Finanzas",
            "",
            f"- Movies con presupuesto informado: **{financial['movies_with_budget']}**.",
            f"- Movies con ingresos informados: **{financial['movies_with_revenue']}**.",
            f"- Movies con ambos campos informados: **{financial['movies_with_both_financial_fields']}**.",
            f"- Cobertura de ambos campos sobre 16.000 Movies: **{financial['movie_financial_coverage_percent']}%**.",
            f"- TV Shows con presupuesto válido: **{financial['tv_shows_with_valid_budget']}**.",
            f"- TV Shows con ingresos válidos: **{financial['tv_shows_with_valid_revenue']}**.",
            f"- Ceros de origen convertidos a NULL: `{financial['source_zero_counts_converted_to_null']}`.",
            "",
            "## Top 10 por contenido distinto",
            "",
            "### Géneros",
            "",
            "| Género | COUNT DISTINCT id_contenido |",
            "|---|---:|",
        ]
    )
    lines.extend(f"| {item['valor']} | {item['count_distinct_id_contenido']} |" for item in report["top_10_generos"])
    lines.extend(["", "### Países", "", "| País | COUNT DISTINCT id_contenido |", "|---|---:|"])
    lines.extend(f"| {item['valor']} | {item['count_distinct_id_contenido']} |" for item in report["top_10_paises"])
    lines.extend(["", "## Checks", "", "| Validación | Resultado |", "|---|---|"])
    lines.extend(f"| `{name}` | {'PASS' if passed else 'FAIL'} |" for name, passed in checks.items())
    lines.extend(
        [
            "",
            "## Alcance predictivo",
            "",
            report["predictive_scope"]["note"],
            "",
            "Los artefactos predictivos existentes se mantienen fuera de `dashboard_contenidos_final.csv`.",
        ]
    )
    VALIDATION_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_readme(report: dict[str, Any]) -> None:
    outputs = report["outputs"]
    lines = [
        "# Fuentes finales para Looker Studio",
        "",
        "Estas fuentes se generan ejecutando `python3 src/pipeline/fuentes_dashboard_finales.py` desde la raíz del proyecto. El pipeline parte directamente de los CSV oficiales en `data/raw/` y no modifica los archivos originales.",
        "",
        "## dashboard_contenidos_final.csv",
        "",
        f"- Granularidad: una fila por contenido ({outputs['dashboard_contenidos_final.csv']['rows']} filas).",
        "- Uso: fuente principal de Looker Studio.",
        "- El identificador `id_contenido` se construye desde `type` y `show_id`; las colisiones dentro del mismo tipo se resuelven con un hash determinista de la fila original.",
        "- No contiene índices ni predicciones del modelado experimental.",
        "",
        "## dashboard_generos.csv",
        "",
        f"- Granularidad: una fila por relación contenido-género ({outputs['dashboard_generos.csv']['rows']} filas).",
        "- Uso: ranking, comparación y análisis correcto de géneros.",
        "- Los géneros se separan por coma, se recortan espacios y se preservan las categorías originales sin fusionarlas.",
        "",
        "## dashboard_paises.csv",
        "",
        f"- Granularidad: una fila por relación contenido-país ({outputs['dashboard_paises.csv']['rows']} filas).",
        "- Uso: mapa y análisis geográfico.",
        "- Los países se separan por coma, se recortan espacios y se mantienen los nombres originales.",
        "",
        "## Origen y tratamiento",
        "",
        "- Movies: `data/raw/netflix_movies_detailed_up_to_2025.csv`.",
        "- TV Shows: `data/raw/netflix_tv_shows_detailed_up_to_2025.csv`.",
        "- La integración es vertical; no se realiza JOIN entre Movies y TV Shows.",
        "- `budget` y `revenue` se conservan únicamente para Movies.",
        "- Los ceros financieros se interpretan como ausencia y se exportan como campos vacíos/NULL.",
        "- No se imputan datos financieros ni se convierten NULL a cero.",
        "- Las relaciones repetidas `id_contenido + categoría` se eliminan de las tablas normalizadas.",
        "",
        "## Validación",
        "",
        "El detalle reproducible está en `dashboard_validation.json` y `dashboard_validation.md`.",
        "",
        "El modelado predictivo existente no se elimina, pero permanece separado. Sus predicciones actuales se generan sobre las 32.000 filas y mezclan observaciones de entrenamiento y prueba; además, `indice_exito` usa variables que también recibe el modelo.",
    ]
    README_FINAL.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    movies = read_source(MOVIES_FILE)
    tv_shows = read_source(TV_FILE)
    raw_rows = movies + tv_shows

    id_info = assign_stable_ids(raw_rows)
    records = build_records(raw_rows, id_info["ids"])
    genre_rows = build_relation_rows(
        records,
        "generos",
        "genero_individual",
        [
            ("tipo", "tipo"),
            ("popularidad", "popularidad"),
            ("votos", "votos"),
            ("valoracion_promedio", "valoracion_promedio"),
            ("anio_publicacion", "anio_publicacion"),
            ("idioma", "idioma"),
            ("pais", "pais"),
        ],
    )
    country_rows = build_relation_rows(
        records,
        "pais",
        "pais_individual",
        [
            ("tipo", "tipo"),
            ("popularidad", "popularidad"),
            ("votos", "votos"),
            ("valoracion_promedio", "valoracion_promedio"),
            ("anio_publicacion", "anio_publicacion"),
            ("idioma", "idioma"),
            ("generos", "generos"),
        ],
    )

    content_rows = sorted(records, key=lambda row: str(row["id_contenido"]))
    write_csv(CONTENT_FILE, CONTENT_FIELDS, content_rows)
    write_csv(GENRES_FILE, GENRE_FIELDS, genre_rows)
    write_csv(COUNTRIES_FILE, COUNTRY_FIELDS, country_rows)

    report = build_validation(raw_rows, content_rows, genre_rows, country_rows, id_info)
    VALIDATION_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_validation_markdown(report)
    write_readme(report)

    print(json.dumps({"status": report["status"], "failed_checks": report["failed_checks"], "outputs": report["outputs"]}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
