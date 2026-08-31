import json
import os
from datetime import datetime, timezone

import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RAW_DIR = os.path.join(ROOT, 'data')
PROCESSED_DIR = os.path.join(ROOT, 'data', 'processed')
DOCS_DIR = os.path.join(ROOT, 'documentation', 'markdown')

DATA_STUDIO_COLUMNS = [
    'show_id',
    'type',
    'title',
    'director',
    'cast',
    'country',
    'date_added',
    'release_year',
    'rating',
    'duration',
    'genres',
    'language',
    'description',
    'popularity',
    'vote_count',
    'vote_average',
    'budget',
    'revenue',
]


def _normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    for column in df.columns:
        if column not in df.columns:
            continue
        if pd.api.types.is_object_dtype(df[column]) or pd.api.types.is_string_dtype(df[column]):
            df[column] = df[column].astype(str).str.strip()
            df.loc[df[column].isin(['nan', 'NaN', 'None', 'none', '']), column] = pd.NA
    return df


def _prepare_dataframe_for_data_studio(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for column in ['budget', 'revenue']:
        if column not in df.columns:
            df[column] = pd.NA

    for column in ['type', 'title', 'director', 'cast', 'country', 'genres', 'language', 'description']:
        if column in df.columns:
            df[column] = df[column].replace({'nan': pd.NA, 'None': pd.NA, 'none': pd.NA})

    df = _normalize_text_columns(df)

    if 'date_added' in df.columns:
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

    if 'country' in df.columns:
        df['country'] = df['country'].where(df['country'].isna(), df['country'].str.title())

    if 'type' in df.columns:
        df['type'] = df['type'].replace({'movie': 'Movie', 'tv show': 'TV Show', 'tv': 'TV Show'})

    return df.reindex(columns=DATA_STUDIO_COLUMNS)


def consolidate_for_data_studio(
    movies_path: str = os.path.join(RAW_DIR, 'netflix_movies_detailed_up_to_2025.csv'),
    tv_path: str = os.path.join(RAW_DIR, 'netflix_tv_shows_detailed_up_to_2025.csv'),
    output_path: str = os.path.join(PROCESSED_DIR, 'catalogo_data_studio.csv'),
    metadata_path: str = os.path.join(PROCESSED_DIR, 'catalogo_data_studio_metadata.json'),
) -> pd.DataFrame:
    """Build a single CSV schema compatible with Google Data Studio.

    The Data Studio issue is that movies and TV datasets don't share the same
    columns. This function normalizes both into one common schema, fills missing
    financial columns for TV shows with nulls, and writes the output in the
    processed folder for any subsequent dashboard work.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    movies = pd.read_csv(movies_path, low_memory=False)
    tv = pd.read_csv(tv_path, low_memory=False)

    movies_clean = _prepare_dataframe_for_data_studio(movies)
    tv_clean = _prepare_dataframe_for_data_studio(tv)

    consolidated = pd.concat([movies_clean, tv_clean], ignore_index=True, sort=False)
    consolidated = consolidated.reindex(columns=DATA_STUDIO_COLUMNS)
    consolidated.to_csv(output_path, index=False)

    metadata = {
        'generated_at_utc': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'source_files': [movies_path, tv_path],
        'output_file': output_path,
        'rows_total': int(len(consolidated)),
        'rows_movies': int(len(movies_clean)),
        'rows_tv': int(len(tv_clean)),
        'columns': DATA_STUDIO_COLUMNS,
        'notes': [
            'The schema is normalized so both movies and TV shows can be loaded in Data Studio without column mismatch errors.',
            'Budget and revenue are kept in the unified schema, but are null for TV show records because the original dataset does not include them.',
            'This file is the canonical dataset to be used by the Data Studio dashboard.'
        ]
    }

    with open(metadata_path, 'w', encoding='utf-8') as metadata_file:
        json.dump(metadata, metadata_file, indent=2, ensure_ascii=False)

    print(f'Unified Data Studio dataset written to: {output_path}')
    print(f'Metadata written to: {metadata_path}')
    print(f'Total rows: {len(consolidated)}')
    return consolidated


if __name__ == '__main__':
    consolidate_for_data_studio()
