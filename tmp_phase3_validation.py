from pathlib import Path
import json
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, mean_squared_error, precision_score, r2_score, recall_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib

project_root = Path.cwd().resolve()
processed_dir = project_root / 'data' / 'processed'
raw_path = processed_dir / 'catalogo_streamview.csv'
df = pd.read_csv(raw_path, low_memory=False)

for column in ['popularity', 'vote_count', 'vote_average', 'budget', 'revenue', 'release_year']:
    df[column] = pd.to_numeric(df[column], errors='coerce')

def min_max(series):
    series = pd.to_numeric(series, errors='coerce')
    min_value = series.min()
    max_value = series.max()
    if pd.isna(min_value) or pd.isna(max_value) or max_value == min_value:
        return pd.Series(0.0, index=series.index)
    return (series - min_value) / (max_value - min_value)

# Target continuous + target class

df['vote_count_log'] = np.log1p(df['vote_count'].fillna(0).clip(lower=0))
df['popularity_norm'] = min_max(df['popularity'].fillna(df['popularity'].median()))
df['vote_count_norm'] = min_max(df['vote_count_log'])
df['vote_average_norm'] = min_max(df['vote_average'].fillna(df['vote_average'].median()))
df['indice_exito'] = (
    0.40 * df['popularity_norm'] +
    0.30 * df['vote_count_norm'] +
    0.30 * df['vote_average_norm']
).clip(0, 1)

df['soporte_valoracion'] = df['vote_count'].ge(100).astype('int8')
low_cut, high_cut = df['indice_exito'].quantile([0.33, 0.66]).tolist()
labels = ['Bajo Exito', 'Medio Exito', 'Alto Exito']
df['categoria_exito'] = pd.cut(
    df['indice_exito'],
    bins=[-np.inf, low_cut, high_cut, np.inf],
    labels=labels,
    right=False,
).astype(str)

feature_columns = [
    'type', 'title', 'country', 'genres', 'language', 'rating',
    'release_year', 'popularity', 'vote_count', 'vote_average',
    'budget', 'revenue', 'soporte_valoracion', 'vote_count_log'
]
feature_columns = [column for column in feature_columns if column in df.columns]

X = df[feature_columns].copy()
y_reg = df['indice_exito'].astype(float)
y_clf = df['categoria_exito']

X_train, X_valid, y_reg_train, y_reg_valid = train_test_split(
    X, y_reg, test_size=0.2, random_state=42
)
_, _, y_clf_train, y_clf_valid = train_test_split(
    X, y_clf, test_size=0.2, random_state=42
)

numeric_cols = X.select_dtypes(include=['number']).columns.tolist()
categorical_cols = [column for column in X.columns if column not in numeric_cols]
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]), numeric_cols),
        ('cat', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')), ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]), categorical_cols),
    ],
    remainder='drop',
)

reg_pipe = Pipeline([
    ('preprocess', preprocessor),
    ('model', LinearRegression()),
])
reg_pipe.fit(X_train, y_reg_train)
reg_pred = reg_pipe.predict(X_valid)
print('regression', {
    'mae': round(mean_absolute_error(y_reg_valid, reg_pred), 4),
    'rmse': round(mean_squared_error(y_reg_valid, reg_pred, squared=False), 4),
    'r2': round(r2_score(y_reg_valid, reg_pred), 4),
})

clf_pipe = Pipeline([
    ('preprocess', preprocessor),
    ('model', RandomForestClassifier(random_state=42, n_estimators=200, class_weight='balanced_subsample')),
])
clf_pipe.fit(X_train, y_clf_train)
clf_pred = clf_pipe.predict(X_valid)
print('classification', {
    'accuracy': round(accuracy_score(y_clf_valid, clf_pred), 4),
    'precision_weighted': round(precision_score(y_clf_valid, clf_pred, average='weighted', zero_division=0), 4),
    'recall_weighted': round(recall_score(y_clf_valid, clf_pred, average='weighted', zero_division=0), 4),
    'f1_weighted': round(f1_score(y_clf_valid, clf_pred, average='weighted', zero_division=0), 4),
})

model_dir = project_root / 'models'
model_dir.mkdir(exist_ok=True)
joblib.dump(reg_pipe, model_dir / 'phase3_validation_regression.pkl')
joblib.dump(clf_pipe, model_dir / 'phase3_validation_classifier.pkl')
print('artifacts', sorted(p.name for p in model_dir.iterdir()))
