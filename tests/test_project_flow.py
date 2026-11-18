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
        'dashboard_contenidos_final.csv',
        'dashboard_generos.csv',
        'dashboard_paises.csv',
        'dashboard_validation.json',
        'dashboard_validation.md',
        'README_fuentes_finales.md',
    }
    actual = {p.name for p in dashboard_dir.iterdir() if p.is_file()}
    assert actual == expected, 'data/dashboard contiene artefactos fuera de la capa final'

    for filename in sorted(name for name in expected if name.endswith('.csv')):
        df = pd.read_csv(dashboard_dir / filename)
        assert not df.empty, f'{filename} está vacío'

    contenidos = pd.read_csv(dashboard_dir / 'dashboard_contenidos_final.csv')
    assert len(contenidos) == 32000
    assert contenidos['id_contenido'].nunique() == 32000

    generos = pd.read_csv(dashboard_dir / 'dashboard_generos.csv')
    paises = pd.read_csv(dashboard_dir / 'dashboard_paises.csv')
    assert generos['genero_individual'].nunique() == 28
    assert paises['pais_individual'].nunique() == 147
    assert not (contenidos['presupuesto'].fillna('').astype(str).str.strip() == '0').any()
    assert not (contenidos['ingresos'].fillna('').astype(str).str.strip() == '0').any()


def test_model_artifact_exists():
    model_path = ROOT / 'models' / 'modelo_final.pkl'
    assert model_path.exists(), 'No existe el artefacto final del modelo'
