from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CANONICAL_DASHBOARD_FILES = {
    'dashboard_ejecutivo.csv',
    'dashboard_contenidos.csv',
    'dashboard_predicciones.csv',
    'README.md',
}

CANONICAL_DATA_FILES = {
    'catalogo_streamview.csv',
    'train_procesado.csv',
    'test_procesado.csv',
}

TEMP_PATTERNS = (
    '*.tmp',
    '*.bak',
    '*.orig',
    '*.log',
    '*.txt',
    '*.pid',
)

ROOT_OBSOLETE_PATTERNS = (
    'tmp_*',
    'tmp.*',
    '*.tmp',
    '*.bak',
    '*.orig',
    '*.log',
)

MODEL_KEEP = {'modelo_final.pkl'}


def delete_matching(root: Path, patterns: tuple[str, ...], keep: set[str] | None = None, skip_dirs: bool = True) -> list[Path]:
    removed: list[Path] = []
    keep = keep or set()
    for path in sorted(root.iterdir()):
        if skip_dirs and path.is_dir():
            continue
        if path.name in keep:
            continue
        if path.name.startswith('tmp_') or any(path.match(pattern) for pattern in patterns):
            if path.exists():
                path.unlink(missing_ok=True)
                removed.append(path)
    return removed


def clean_dashboard_exports(dashboard_dir: Path) -> list[Path]:
    removed: list[Path] = []
    for path in sorted(dashboard_dir.iterdir()):
        if not path.is_file():
            continue
        if path.name in CANONICAL_DASHBOARD_FILES:
            continue
        if path.suffix.lower() == '.csv' or path.name.endswith('_old.csv') or path.name.startswith('metrics_'):
            path.unlink(missing_ok=True)
            removed.append(path)
    return removed


def clean_processed_data(processed_dir: Path) -> list[Path]:
    removed: list[Path] = []
    for path in sorted(processed_dir.iterdir()):
        if not path.is_file():
            continue
        if path.name in CANONICAL_DATA_FILES:
            continue
        if path.suffix.lower() == '.csv':
            path.unlink(missing_ok=True)
            removed.append(path)
    return removed


def clean_model_directory(models_dir: Path) -> list[Path]:
    removed: list[Path] = []
    for path in sorted(models_dir.iterdir()):
        if not path.is_file():
            continue
        if path.name in MODEL_KEEP:
            continue
        if path.suffix.lower() in {'.pkl', '.json'}:
            path.unlink(missing_ok=True)
            removed.append(path)
    return removed


def main() -> None:
    parser = argparse.ArgumentParser(description='Limpia artefactos temporales, modelos obsoletos y exportaciones del proyecto que ya no deben usarse.')
    parser.add_argument('--root', type=str, default=str(ROOT), help='Ruta base del proyecto')
    parser.add_argument('--dry-run', action='store_true', help='Muestra lo que se eliminaría sin borrarlo')
    args = parser.parse_args()

    project_root = Path(args.root).resolve()
    dashboard_dir = project_root / 'data' / 'dashboard'
    processed_dir = project_root / 'data' / 'processed'
    models_dir = project_root / 'models'

    removed: list[Path] = []
    removed.extend(delete_matching(project_root, ROOT_OBSOLETE_PATTERNS))

    if dashboard_dir.exists():
        removed.extend(clean_dashboard_exports(dashboard_dir))
    if processed_dir.exists():
        removed.extend(clean_processed_data(processed_dir))
    if models_dir.exists():
        removed.extend(clean_model_directory(models_dir))

    if not removed:
        print('No se encontraron artefactos temporales o obsoletos para eliminar.')
    else:
        print('Se eliminaron los siguientes artefactos:')
        for item in removed:
            print(f'- {item.relative_to(project_root)}')

    if dashboard_dir.exists():
        current_dash = sorted(p.name for p in dashboard_dir.iterdir() if p.is_file())
        print(f'Archivos actuales en data/dashboard: {current_dash}')
    if processed_dir.exists():
        current_processed = sorted(p.name for p in processed_dir.iterdir() if p.is_file())
        print(f'Archivos actuales en data/processed: {current_processed}')
    if models_dir.exists():
        current_models = sorted(p.name for p in models_dir.iterdir() if p.is_file())
        print(f'Archivos actuales en models: {current_models}')


if __name__ == '__main__':
    main()
