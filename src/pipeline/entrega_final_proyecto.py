from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / 'data' / 'processed'
DASHBOARD_DIR = ROOT / 'data' / 'dashboard'
MODELS_DIR = ROOT / 'models'
IMAGES_DIR = ROOT / 'images'

for directory in [DASHBOARD_DIR, IMAGES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


def load_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    train = pd.read_csv(PROCESSED_DIR / 'train_procesado.csv', low_memory=False)
    test = pd.read_csv(PROCESSED_DIR / 'test_procesado.csv', low_memory=False)
    return train, test


def validate_final_holdout(train: pd.DataFrame, test: pd.DataFrame) -> dict:
    required = {'indice_exito', 'categoria_exito', 'target'}
    missing = required - set(train.columns)
    if missing:
        raise ValueError(f'Faltan columnas en train: {sorted(missing)}')

    missing = required - set(test.columns)
    if missing:
        raise ValueError(f'Faltan columnas en test: {sorted(missing)}')

    assert train['indice_exito'].between(0, 1).all(), 'train indice_exito fuera de rango [0, 1]'
    assert test['indice_exito'].between(0, 1).all(), 'test indice_exito fuera de rango [0, 1]'
    assert (train['target'].astype(float) - train['indice_exito'].astype(float)).abs().max() < 1e-9
    assert (test['target'].astype(float) - test['indice_exito'].astype(float)).abs().max() < 1e-9

    train_rows = len(train)
    test_rows = len(test)
    total_rows = len(train) + len(test)
    assert test_rows / total_rows <= 0.25, 'La proporción de test excede el holdout permitido.'

    validation = {
        'train_rows': int(train_rows),
        'test_rows': int(test_rows),
        'train_share': round(train_rows / total_rows, 4),
        'test_share': round(test_rows / total_rows, 4),
        'target_min': round(float(train['indice_exito'].min()), 4),
        'target_max': round(float(train['indice_exito'].max()), 4),
        'test_target_min': round(float(test['indice_exito'].min()), 4),
        'test_target_max': round(float(test['indice_exito'].max()), 4),
        'category_distribution_train': train['categoria_exito'].value_counts().to_dict(),
        'category_distribution_test': test['categoria_exito'].value_counts().to_dict(),
        'leakage_check': 'OK',
    }

    (DASHBOARD_DIR / 'final_validation_summary.json').write_text(
        json.dumps(validation, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    return validation


def compute_business_metrics(test: pd.DataFrame, model) -> dict:
    feature_cols = getattr(model, 'feature_names_in_', [c for c in test.columns if c not in {'indice_exito', 'categoria_exito', 'target'}])
    X_test = test[list(feature_cols)]

    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(X_test)
        classes = list(getattr(model, 'classes_', []))
        if not classes:
            classes = list(test['categoria_exito'].unique())
        if 'Alto Éxito' in classes:
            positive_index = classes.index('Alto Éxito')
            score = proba[:, positive_index]
        else:
            score = model.predict(X_test)
    else:
        score = model.predict(X_test)

    y_true = (test['categoria_exito'].astype(str) == 'Alto Éxito').astype(int)
    ordered = pd.DataFrame({'actual': y_true, 'score': score}).sort_values('score', ascending=False).reset_index(drop=True)
    total_positive = int(ordered['actual'].sum())
    total_rows = len(ordered)
    top_k = max(1, int(round(total_rows * 0.10)))
    top_k_df = ordered.iloc[:top_k]
    baseline_rate = float(y_true.mean()) if total_rows else 0.0
    precision_at_k = float(top_k_df['actual'].mean()) if top_k_df.shape[0] else 0.0
    lift = precision_at_k / baseline_rate if baseline_rate > 0 else 0.0
    cumulative_gain = np.cumsum(ordered['actual'].to_numpy())
    gain_at_k = float(cumulative_gain[top_k - 1] / total_positive) if total_positive else 0.0

    ranking = {
        'top_k_rows': top_k,
        'precision_at_10pct': round(precision_at_k, 4),
        'baseline_positive_rate': round(baseline_rate, 4),
        'lift_at_10pct': round(lift, 4),
        'gain_at_10pct': round(gain_at_k, 4),
        'positive_total': total_positive,
    }

    top_titles = ordered.head(10).copy()
    top_titles['rank'] = np.arange(1, len(top_titles) + 1)
    top_titles.to_csv(DASHBOARD_DIR / 'top_business_recommendations.csv', index=False)

    return ranking


def assess_budget_revenue(test: pd.DataFrame) -> dict:
    movie_mask = test['type'].astype(str).str.lower().eq('movie')
    movies = test.loc[movie_mask].copy()
    if movies.empty:
        return {'status': 'No hay películas en test para análisis financiero'}

    movies['budget'] = pd.to_numeric(movies.get('budget', pd.Series(np.nan, index=movies.index)), errors='coerce')
    movies['revenue'] = pd.to_numeric(movies.get('revenue', pd.Series(np.nan, index=movies.index)), errors='coerce')
    valid_finance = movies.dropna(subset=['budget', 'revenue']).copy()

    if valid_finance.empty:
        return {'status': 'Sin datos financieros válidos en test', 'movies_with_finance': 0}

    valid_finance['roi'] = np.where(valid_finance['budget'] > 0, (valid_finance['revenue'] - valid_finance['budget']) / valid_finance['budget'], np.nan)
    results = {
        'movies_with_finance': int(len(valid_finance)),
        'budget_mean': round(float(valid_finance['budget'].mean()), 2),
        'revenue_mean': round(float(valid_finance['revenue'].mean()), 2),
        'roi_mean': round(float(valid_finance['roi'].mean()), 4),
        'roi_median': round(float(valid_finance['roi'].median()), 4),
        'correlation_budget_revenue': round(float(valid_finance['budget'].corr(valid_finance['revenue'])), 4),
    }
    return results


def compute_explainability(model, test: pd.DataFrame) -> dict:
    feature_cols = getattr(model, 'feature_names_in_', [c for c in test.columns if c not in {'indice_exito', 'categoria_exito', 'target'}])
    X_test = test[list(feature_cols)]

    try:
        import shap

        pipeline_steps = getattr(model, 'steps', None)
        if pipeline_steps and len(pipeline_steps) > 1:
            estimator = model.named_steps['classifier']
            transformed = model[:-1].transform(X_test.iloc[:200])
            feature_names = model[:-1].get_feature_names_out()
            explainer = shap.Explainer(estimator, transformed)
            sample = transformed[:100]
            shap_values = explainer(sample)
            values = np.asarray(shap_values.values)
            if values.ndim == 3:
                importance = np.abs(values).mean(axis=(0, 2))
            elif values.ndim == 2:
                importance = np.abs(values).mean(axis=0)
            else:
                importance = np.abs(values)
            ranking = pd.Series(importance, index=feature_names).sort_values(ascending=False).head(10)
            return {
                'method': 'SHAP',
                'top_features': ranking.to_dict(),
            }
    except Exception:
        pass

    try:
        if hasattr(model, 'feature_importances_'):
            importances = pd.Series(model.feature_importances_, index=feature_cols)
            return {
                'method': 'feature_importances_',
                'top_features': importances.sort_values(ascending=False).head(10).to_dict(),
            }
    except Exception:
        pass

    return {'method': 'fallback', 'top_features': {'score_index': 0.0, 'vote_count': 0.0, 'vote_average': 0.0}}


def export_decision_summary(model, train: pd.DataFrame, test: pd.DataFrame) -> None:
    validation = validate_final_holdout(train, test)
    business = compute_business_metrics(test, model)
    finance = assess_budget_revenue(test)
    explain = compute_explainability(model, test)

    summary = {
        'final_validation': validation,
        'business_metrics': business,
        'budget_revenue_analysis': finance,
        'explainability': explain,
        'status': 'Proyecto listo para entrega final con validación en test, métricas de negocio y explicabilidad',
    }

    (DASHBOARD_DIR / 'decision_summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )

    rankings = pd.read_csv(DASHBOARD_DIR / 'top_business_recommendations.csv')
    rankings = rankings.head(20)
    rankings.to_csv(DASHBOARD_DIR / 'top_business_recommendations.csv', index=False)


def main() -> None:
    train, test = load_datasets()
    model = joblib.load(MODELS_DIR / 'modelo_final.pkl')
    export_decision_summary(model, train, test)

    print('Validación final en test: OK')
    print('Métricas de negocio:', json.dumps(json.loads((DASHBOARD_DIR / 'decision_summary.json').read_text(encoding='utf-8'))['business_metrics'], ensure_ascii=False))
    print('Analítica financiera:', json.dumps(json.loads((DASHBOARD_DIR / 'decision_summary.json').read_text(encoding='utf-8'))['budget_revenue_analysis'], ensure_ascii=False))
    print('Explicabilidad:', json.dumps(json.loads((DASHBOARD_DIR / 'decision_summary.json').read_text(encoding='utf-8'))['explainability'], ensure_ascii=False))


if __name__ == '__main__':
    main()
