from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def find_project_root() -> Path:
    current = Path.cwd().resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "data" / "processed" / "catalogo_streamview.csv").exists():
            return candidate
    raise FileNotFoundError("No se encontró la raíz del proyecto con data/processed/catalogo_streamview.csv")


def prepare_targets(df: pd.DataFrame) -> pd.DataFrame:
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
    df["vote_count_log"] = np.log1p(df["vote_count"].fillna(0).clip(lower=0))
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
        bins=[-np.inf, low_cut, high_cut, np.inf],
        labels=labels,
        right=False,
    ).astype(str)
    df["categoria_exito"] = df["categoria_exito"].fillna("Medio Éxito")

    # El target del modelo está definido por la métrica de éxito, no por la columna type.
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


def build_preprocessor(X: pd.DataFrame, max_categories: int = 25):
    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = [col for col in X.columns if col not in numeric_cols]

    transformers = [
        (
            "num",
            Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]),
            numeric_cols,
        ),
        (
            "cat",
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    (
                        "onehot",
                        OneHotEncoder(
                            handle_unknown="ignore",
                            sparse_output=False,
                            max_categories=max_categories,
                        ),
                    ),
                ]
            ),
            categorical_cols,
        ),
    ]

    return ColumnTransformer(transformers=transformers, remainder="drop")


def compute_metrics_regression(y_true, y_pred):
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
    }


def compute_metrics_classification(y_true, y_pred):
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision_weighted": float(precision_score(y_true, y_pred, average="weighted", zero_division=0)),
        "recall_weighted": float(recall_score(y_true, y_pred, average="weighted", zero_division=0)),
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
    }


def train_baselines(X_train, X_valid, y_reg_train, y_reg_valid, y_clf_train, y_clf_valid, max_categories: int):
    preprocessor = build_preprocessor(X_train, max_categories=max_categories)

    reg_pipe = Pipeline(
        [
            ("preprocess", preprocessor),
            ("model", LinearRegression()),
        ]
    )
    reg_pipe.fit(X_train, y_reg_train)
    reg_pred = reg_pipe.predict(X_valid)

    clf_pipe = Pipeline(
        [
            ("preprocess", preprocessor),
            (
                "model",
                RandomForestClassifier(
                    random_state=42,
                    n_estimators=200,
                    class_weight="balanced_subsample",
                    n_jobs=-1,
                ),
            ),
        ]
    )
    clf_pipe.fit(X_train, y_clf_train)
    clf_pred = clf_pipe.predict(X_valid)

    return {
        "regression": compute_metrics_regression(y_reg_valid, reg_pred),
        "classification": compute_metrics_classification(y_clf_valid, clf_pred),
        "models": {"regression": reg_pipe, "classification": clf_pipe},
    }


def train_full_tuned(X_train, X_valid, y_reg_train, y_reg_valid, y_clf_train, y_clf_valid, max_categories: int):
    preprocessor = build_preprocessor(X_train, max_categories=max_categories)

    reg_pipeline = Pipeline([
        ("preprocess", preprocessor),
        ("model", RandomForestRegressor(random_state=42, n_jobs=-1)),
    ])
    reg_grid = {
        "model__n_estimators": [200],
        "model__max_depth": [None, 10],
        "model__min_samples_leaf": [1, 2],
    }

    clf_pipeline = Pipeline([
        ("preprocess", preprocessor),
        ("model", RandomForestClassifier(random_state=42, n_jobs=-1)),
    ])
    clf_grid = {
        "model__n_estimators": [200],
        "model__max_depth": [None, 10],
        "model__min_samples_leaf": [1, 2],
        "model__class_weight": ["balanced", "balanced_subsample"],
    }

    grid_reg = GridSearchCV(
        reg_pipeline,
        param_grid=reg_grid,
        cv=2,
        n_jobs=1,
        scoring="neg_mean_absolute_error",
    )
    grid_clf = GridSearchCV(
        clf_pipeline,
        param_grid=clf_grid,
        cv=2,
        n_jobs=1,
        scoring="f1_weighted",
    )

    grid_reg.fit(X_train, y_reg_train)
    grid_clf.fit(X_train, y_clf_train)
    reg_pred = grid_reg.best_estimator_.predict(X_valid)
    clf_pred = grid_clf.best_estimator_.predict(X_valid)

    return {
        "regression": compute_metrics_regression(y_reg_valid, reg_pred),
        "classification": compute_metrics_classification(y_clf_valid, clf_pred),
        "models": {
            "regression": grid_reg.best_estimator_,
            "classification": grid_clf.best_estimator_,
        },
        "grid": {
            "regression": grid_reg.best_params_,
            "classification": grid_clf.best_params_,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Pipeline rápido de Fase 3 para StreamView Analytics")
    parser.add_argument("--full-tuning", action="store_true", help="Ejecuta GridSearch, pero solo si se quiere comparar rendimiento y no en modo de validación rápida.")
    parser.add_argument("--max-categories", type=int, default=25, help="Límite de categorías en OneHot para evitar explosión de columnas.")
    args = parser.parse_args()

    project_root = find_project_root()
    processed_dir = project_root / "data" / "processed"
    df = pd.read_csv(processed_dir / "catalogo_streamview.csv", low_memory=False)
    df = prepare_targets(df)
    X, y_reg, y_clf = build_modeling_frame(df)

    X_train, X_valid, y_reg_train, y_reg_valid = train_test_split(X, y_reg, test_size=0.2, random_state=42)
    _, _, y_clf_train, y_clf_valid = train_test_split(X, y_clf, test_size=0.2, random_state=42)

    if args.full_tuning:
        result = train_full_tuned(
            X_train,
            X_valid,
            y_reg_train,
            y_reg_valid,
            y_clf_train,
            y_clf_valid,
            max_categories=args.max_categories,
        )
    else:
        result = train_baselines(
            X_train,
            X_valid,
            y_reg_train,
            y_reg_valid,
            y_clf_train,
            y_clf_valid,
            max_categories=args.max_categories,
        )

    model_dir = project_root / "models"
    model_dir.mkdir(exist_ok=True)

    joblib.dump(result["models"]["regression"], model_dir / "best_regression_model.pkl")
    joblib.dump(result["models"]["classification"], model_dir / "best_classifier_model.pkl")

    payload = {
        "regression": result["regression"],
        "classification": result["classification"],
    }
    if "grid" in result:
        payload["grid"] = result["grid"]

    with (model_dir / "phase3_model_results.json").open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
