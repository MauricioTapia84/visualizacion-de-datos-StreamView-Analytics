from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "processed"
CATALOGO_PATH = PROCESSED_DIR / "catalogo_streamview.csv"
TRAIN_PATH = PROCESSED_DIR / "train_procesado.csv"
TEST_PATH = PROCESSED_DIR / "test_procesado.csv"


def min_max(series: pd.Series) -> pd.Series:
    series = pd.to_numeric(series, errors="coerce")
    min_value = series.min()
    max_value = series.max()
    if pd.isna(min_value) or pd.isna(max_value) or max_value == min_value:
        return pd.Series(0.0, index=series.index)
    return (series - min_value) / (max_value - min_value)


def compute_success_target(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for column in ["popularity", "vote_count", "vote_average", "budget", "revenue", "release_year"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df["vote_count_log"] = np.log1p(df["vote_count"].fillna(0).clip(lower=0))
    popularity_median = df["popularity"].median()
    vote_average_median = df["vote_average"].median()

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

    lower_cut, upper_cut = df["indice_exito"].quantile([0.33, 0.66]).tolist()
    labels = ["Bajo Éxito", "Medio Éxito", "Alto Éxito"]
    df["categoria_exito"] = pd.cut(
        df["indice_exito"],
        bins=[-np.inf, lower_cut, upper_cut, np.inf],
        labels=labels,
        right=False,
    ).astype(str)
    df["categoria_exito"] = df["categoria_exito"].fillna("Medio Éxito")

    return df


def build_holdout_split(df: pd.DataFrame, test_size: float = 0.20, random_state: int = 42):
    if "categoria_exito" not in df.columns:
        raise ValueError("Necesario crear categoria_exito antes del split.")

    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df["categoria_exito"],
    )

    return train_df.reset_index(drop=True), test_df.reset_index(drop=True)


def main() -> None:
    if not CATALOGO_PATH.exists():
        raise FileNotFoundError(f"No existe el dataset base: {CATALOGO_PATH}")

    df = pd.read_csv(CATALOGO_PATH, low_memory=False)
    df = compute_success_target(df)
    train_df, test_df = build_holdout_split(df)

    train_df.to_csv(TRAIN_PATH, index=False)
    test_df.to_csv(TEST_PATH, index=False)

    print(f"Target formalizado: indice_exito y categoria_exito")
    print(f"Train rows: {len(train_df)}")
    print(f"Test rows: {len(test_df)}")
    print(f"Clase mayoritaria: {train_df['categoria_exito'].mode().iloc[0]}")


if __name__ == "__main__":
    main()
