from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def test_processed_data_exists():
    train = ROOT / 'data' / 'processed' / 'train_procesado.csv'
    test = ROOT / 'data' / 'processed' / 'test_procesado.csv'
    assert train.exists(), 'Falta train_procesado.csv'
    assert test.exists(), 'Falta test_procesado.csv'

    train_df = pd.read_csv(train)
    test_df = pd.read_csv(test)

    assert 'indice_exito' in train_df.columns
    assert 'indice_exito' in test_df.columns
    assert train_df['indice_exito'].between(0, 1).all()
    assert test_df['indice_exito'].between(0, 1).all()


def test_dashboard_exports_are_current():
    dashboard_dir = ROOT / 'data' / 'dashboard'
    expected = {
        'dashboard_ejecutivo.csv',
        'dashboard_contenidos.csv',
        'dashboard_predicciones.csv',
    }
    actual = {p.name for p in dashboard_dir.iterdir() if p.is_file() and p.suffix.lower() == '.csv'}
    assert expected.issubset(actual), 'Faltan los CSVs actuales para Data Studio'

    for filename in sorted(expected):
        df = pd.read_csv(dashboard_dir / filename)
        assert not df.empty, f'{filename} está vacío'


def test_model_artifact_exists():
    model_path = ROOT / 'models' / 'modelo_final.pkl'
    assert model_path.exists(), 'No existe el artefacto final del modelo'
