import os
import pandas as pd
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RAW_DIR = os.path.join(ROOT, 'data')
PROCESSED_DIR = os.path.join(ROOT, 'data', 'processed')
DOCS_DIR = os.path.join(ROOT, 'documentation', 'markdown')

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

FILES = [
    ('movies', os.path.join(RAW_DIR, 'netflix_movies_detailed_up_to_2025.csv')),
    ('tv', os.path.join(RAW_DIR, 'netflix_tv_shows_detailed_up_to_2025.csv')),
]

summary = {
    'run_date': datetime.utcnow().isoformat() + 'Z',
    'files': {}
}

for key, path in FILES:
    info = {'path': path}
    if not os.path.exists(path):
        info['error'] = 'file not found'
        summary['files'][key] = info
        continue
    print(f'Reading {path}...')
    df = pd.read_csv(path, low_memory=False)
    info['original_rows'] = int(len(df))

    # Duplicates (consider full-row duplicates and also show_id if exists)
    full_dup = int(df.duplicated().sum())
    info['full_row_duplicates'] = full_dup
    if 'show_id' in df.columns:
        id_dup = int(df.duplicated(subset=['show_id']).sum())
        info['show_id_duplicates'] = id_dup
    else:
        info['show_id_duplicates'] = None

    # Initial cleaning steps
    # 1) Drop full-row duplicates
    df = df.drop_duplicates()
    after_dup_rows = int(len(df))
    info['rows_after_dedup'] = after_dup_rows

    # 2) Normalize whitespace in object columns
    obj_cols = df.select_dtypes(include=['object']).columns.tolist()
    for c in obj_cols:
        try:
            df[c] = df[c].astype(str).str.strip()
            df.loc[df[c] == 'nan', c] = pd.NA
        except Exception:
            pass

    # 3) Parse `date_added` if present
    if 'date_added' in df.columns:
        parsed = pd.to_datetime(df['date_added'], errors='coerce')
        info['date_added_parsed_nulls_before'] = int(df['date_added'].isnull().sum())
        df['date_added'] = parsed
        info['date_added_parsed_nulls_after'] = int(df['date_added'].isnull().sum())

    # 4) Lowercase countries
    if 'country' in df.columns:
        df['country'] = df['country'].where(df['country'].isna(), df['country'].str.title())

    # 5) Replace empty strings with NA and count nulls
    df = df.replace({'': pd.NA, 'None': pd.NA, 'nan': pd.NA})

    null_counts = df.isnull().sum().sort_values(ascending=False)
    info['null_counts_top10'] = null_counts.head(10).to_dict()
    info['total_nulls'] = int(null_counts.sum())

    # Save processed CSV
    out_path = os.path.join(PROCESSED_DIR, f'{key}_processed.csv')
    df.to_csv(out_path, index=False)
    info['processed_path'] = out_path
    info['processed_rows'] = int(len(df))

    summary['files'][key] = info

# Write a markdown report
md_path = os.path.join(DOCS_DIR, 'EP1_data_cleaning.md')
print(f'Writing report to {md_path}...')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write('---\n')
    f.write("title: \"EP1 — Data cleaning inicial\"\n")
    f.write("author: \"Equipo StreamView (script)\"\n")
    f.write(f"date: {datetime.utcnow().date()}\n")
    f.write("source_files:\n")
    for _, p in FILES:
        f.write(f"  - {os.path.relpath(p, ROOT)}\n")
    f.write('---\n\n')
    f.write('# Resumen de la limpieza inicial\n\n')
    f.write(f'Fecha de ejecución (UTC): {summary["run_date"]}\n\n')

    for key, info in summary['files'].items():
        f.write(f'## Archivo: {key}\n\n')
        if 'error' in info:
            f.write(f'- Error: {info["error"]}\n\n')
            continue
        f.write(f'- Ruta original: {info["path"]}\n')
        f.write(f'- Filas originales: {info.get("original_rows")}\n')
        f.write(f'- Filas después de eliminar duplicados: {info.get("rows_after_dedup")}\n')
        f.write(f'- Duplicados (filas completas): {info.get("full_row_duplicates")}\n')
        if info.get('show_id_duplicates') is not None:
            f.write(f'- Duplicados por `show_id`: {info.get("show_id_duplicates")}\n')
        if 'date_added_parsed_nulls_before' in info:
            f.write(f'- `date_added` nulos antes: {info.get("date_added_parsed_nulls_before")}\n')
            f.write(f'- `date_added` nulos después de parseo: {info.get("date_added_parsed_nulls_after")}\n')
        f.write(f'- Filas procesadas guardadas en: {os.path.relpath(info.get("processed_path"), ROOT)}\n')
        f.write(f'- Total de valores nulos (suma por columnas): {info.get("total_nulls")}\n')
        f.write('\n')
        f.write('### Top 10 columnas por valores faltantes\n\n')
        f.write('| Columna | Nulos |\n')
        f.write('|---|---:|\n')
        for col, n in info.get('null_counts_top10', {}).items():
            f.write(f'| {col} | {n} |\n')
        f.write('\n')

print('Done.')
