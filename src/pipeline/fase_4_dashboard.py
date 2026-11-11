from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


def find_project_root() -> Path:
    current = Path.cwd().resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "data" / "processed" / "catalogo_streamview.csv").exists():
            return candidate
    raise FileNotFoundError("No se encontró la raíz del proyecto con data/processed/catalogo_streamview.csv")


def prepare_targets(df: pd.DataFrame) -> pd.DataFrame:
    if "id_contenido" not in df.columns:
        df["id_contenido"] = np.arange(1, len(df) + 1)

    for column in ["popularity", "vote_count", "vote_average", "budget", "revenue", "release_year"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    def min_max(series: pd.Series) -> pd.Series:
        series = pd.to_numeric(series, errors="coerce")
        min_value = series.min()
        max_value = series.max()
        if pd.isna(min_value) or pd.isna(max_value) or max_value == min_value:
            return pd.Series(0.0, index=series.index)
        return (series - min_value) / (max_value - min_value)

    popularity_median = df["popularity"].median()
    vote_average_median = df["vote_average"].median()
    df["vote_count_log"] = df["vote_count"].fillna(0).clip(lower=0).apply(np.log1p)
    df["popularity_norm"] = min_max(df["popularity"].fillna(popularity_median))
    df["vote_count_norm"] = min_max(df["vote_count_log"])
    df["vote_average_norm"] = min_max(df["vote_average"].fillna(vote_average_median))

    df["indice_exito"] = (
        0.40 * df["popularity_norm"]
        + 0.30 * df["vote_count_norm"]
        + 0.30 * df["vote_average_norm"]
    ).clip(0, 1)

    df["target"] = df["indice_exito"].copy()
    df["soporte_valoracion"] = df["vote_count"].ge(100).astype("int8")

    low_cut, high_cut = df["indice_exito"].quantile([0.33, 0.66]).tolist()
    labels = ["Bajo Éxito", "Medio Éxito", "Alto Éxito"]
    df["categoria_exito"] = pd.cut(
        df["indice_exito"],
        bins=[-float("inf"), low_cut, high_cut, float("inf")],
        labels=labels,
        right=False,
    ).astype(str)
    df["categoria_exito"] = df["categoria_exito"].fillna("Medio Éxito")

    # El target del modelo debe estar definido por la métrica de éxito y no por la columna type.
    if "type" in df.columns:
        df["type"] = df["type"].astype(str)

    return df


def build_modeling_frame(df: pd.DataFrame):
    feature_columns = [
        "type",
        "title",
        "country",
        "genres",
        "language",
        "rating",
        "release_year",
        "popularity",
        "vote_count",
        "vote_average",
        "budget",
        "revenue",
        "soporte_valoracion",
        "vote_count_log",
    ]
    feature_columns = [col for col in feature_columns if col in df.columns]
    X = df[feature_columns].copy()
    y_reg = df["indice_exito"].astype(float)
    y_clf = df["categoria_exito"]
    return X, y_reg, y_clf


def build_dashboard_outputs(project_root: Path):
    processed_dir = project_root / "data" / "processed"
    model_dir = project_root / "models"

    df = pd.read_csv(processed_dir / "catalogo_streamview.csv", low_memory=False)
    if "id_contenido" not in df.columns:
        df["id_contenido"] = np.arange(1, len(df) + 1)
    df = prepare_targets(df)
    X, _, _ = build_modeling_frame(df)

    reg_model = joblib.load(model_dir / "best_regression_model.pkl")
    clf_model = joblib.load(model_dir / "best_classifier_model.pkl")

    pred_score = reg_model.predict(X)
    pred_label = clf_model.predict(X)

    df["pred_indice_exito"] = pred_score
    df["pred_categoria_exito"] = pred_label
    df["prioridad_prediccion"] = df["pred_indice_exito"].rank(method="first", ascending=False).astype(int)

    executive = (
        df.groupby(["type", "pred_categoria_exito"], dropna=False)
        .agg(
            titulos=("title", "count"),
            score_promedio=("pred_indice_exito", "mean"),
            popularidad_media=("popularity", "mean"),
            rating_medio=("vote_average", "mean"),
            contenidos_altos=("pred_indice_exito", lambda s: int((s >= 0.75).sum())),
        )
        .reset_index()
        .sort_values(["type", "score_promedio"], ascending=[True, False])
    )
    executive.columns = [
        "tipo",
        "categoria_predicha",
        "titulos",
        "score_promedio",
        "popularidad_media",
        "rating_medio",
        "contenidos_altos",
    ]
    executive.to_csv(processed_dir / "dashboard_ejecutivo.csv", index=False)

    contenidos = df[
        [
            "id_contenido",
            "title",
            "type",
            "genres",
            "country",
            "language",
            "release_year",
            "popularity",
            "vote_count",
            "vote_average",
            "indice_exito",
            "categoria_exito",
            "pred_indice_exito",
            "pred_categoria_exito",
        ]
    ].copy()
    contenidos = contenidos.sort_values("pred_indice_exito", ascending=False).reset_index(drop=True)
    contenidos.columns = [
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
        "indice_exito",
        "categoria_exito",
        "pred_indice_exito",
        "pred_categoria_exito",
    ]
    contenidos.to_csv(processed_dir / "dashboard_contenidos.csv", index=False)

    predicciones = df[
        [
            "id_contenido",
            "title",
            "type",
            "genres",
            "country",
            "release_year",
            "pred_indice_exito",
            "pred_categoria_exito",
            "indice_exito",
            "categoria_exito",
        ]
    ].copy()
    predicciones.columns = [
        "id_contenido",
        "titulo",
        "tipo",
        "generos",
        "pais",
        "anio_publicacion",
        "score_predicho",
        "categoria_predicha",
        "indice_exito_real",
        "categoria_exito_real",
    ]
    predicciones = predicciones.sort_values("score_predicho", ascending=False).reset_index(drop=True)
    predicciones.to_csv(processed_dir / "dashboard_predicciones.csv", index=False)

    metric_summary = json.loads((model_dir / "phase3_model_results.json").read_text(encoding="utf-8"))
    summary = {
        "filas_catalogo": int(len(df)),
        "tipos": sorted(df["type"].dropna().unique().tolist()),
        "score_promedio": float(df["pred_indice_exito"].mean()),
        "top_titulo": df.loc[df["pred_indice_exito"].idxmax(), "title"],
        "metrics": metric_summary,
    }
    (project_root / "data" / "processed" / "fase4_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return executive, contenidos, predicciones


def write_dashboard_html(project_root: Path):
    processed_dir = project_root / "data" / "processed"
    executive = pd.read_csv(processed_dir / "dashboard_ejecutivo.csv")
    contenidos = pd.read_csv(processed_dir / "dashboard_contenidos.csv")
    metrics = json.loads((processed_dir / "fase4_summary.json").read_text(encoding="utf-8"))

    total_titles = int(executive["titulos"].sum()) if not executive.empty else 0
    avg_score = float((executive["score_promedio"].mean()) if not executive.empty else 0)
    top_titles = contenidos.head(10).to_dict(orient="records")

    rows = "\n".join(
        f"<tr><td>{row['titulo']}</td><td>{row['tipo']}</td><td>{float(row['pred_indice_exito']):.3f}</td><td>{row['pred_categoria_exito']}</td></tr>"
        for row in top_titles
    )

    html = f"""<!DOCTYPE html>
<html lang=\"es\">
<head>
  <meta charset=\"utf-8\" />
  <title>StreamView Analytics - Dashboard predictivo</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; background: #f6f8fb; color: #1f2937; }}
    .container {{ max-width: 1200px; margin: 0 auto; }}
    .header {{ margin-bottom: 24px; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 16px; margin-bottom: 24px; }}
    .card {{ background: white; border-radius: 12px; padding: 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }}
    .label {{ color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; }}
    .value {{ font-size: 28px; font-weight: bold; margin-top: 6px; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid #e5e7eb; text-align: left; }}
    th {{ background: #eff6ff; }}
    h2 {{ margin-bottom: 12px; }}
  </style>
</head>
<body>
  <div class=\"container\">
    <div class=\"header\">
      <h1>StreamView Analytics</h1>
      <p>Dashboard predictivo final con priorización de contenidos por potencial de éxito futuro.</p>
    </div>

    <div class=\"grid\">
      <div class=\"card\"><div class=\"label\">Catálogo total</div><div class=\"value\">{metrics['filas_catalogo']:,}</div></div>
      <div class=\"card\"><div class=\"label\">Tipos</div><div class=\"value\">{', '.join(metrics['tipos'])}</div></div>
      <div class=\"card\"><div class=\"label\">Score promedio</div><div class=\"value\">{avg_score:.3f}</div></div>
      <div class=\"card\"><div class=\"label\">Máximo potencial</div><div class=\"value\">{metrics['top_titulo']}</div></div>
    </div>

    <h2>Top títulos por score previsto</h2>
    <table>
      <thead>
        <tr><th>Título</th><th>Tipo</th><th>Score</th><th>Categoria</th></tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>

    <h2>Resumen del modelo</h2>
    <div class=\"card\">
      <p>Regresión: MAE {metrics['metrics']['regression']['mae']:.6f} | RMSE {metrics['metrics']['regression']['rmse']:.6f} | R² {metrics['metrics']['regression']['r2']:.6f}</p>
      <p>Clasificación: Accuracy {metrics['metrics']['classification']['accuracy']:.6f} | F1 weighted {metrics['metrics']['classification']['f1_weighted']:.6f}</p>
    </div>
  </div>
</body>
</html>
"""

    output_path = project_root / "images" / "dashboard_streamview.html"
    output_path.write_text(html, encoding="utf-8")
    return output_path


def main():
    project_root = find_project_root()
    build_dashboard_outputs(project_root)
    html_path = write_dashboard_html(project_root)
    print(f"Fase 4 generada en: {project_root}")
    print(f"Dashboard HTML: {html_path}")
    print("CSVs creados: dashboard_ejecutivo.csv, dashboard_contenidos.csv, dashboard_predicciones.csv")


if __name__ == "__main__":
    main()
