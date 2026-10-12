from pathlib import Path
import pandas as pd

path = Path("c:/Users/admin/Documents/GitHub/visualizacion-de-datos-StreamView-Analytics/data/processed/catalogo_streamview.csv")
df = pd.read_csv(path, encoding='utf-8-sig', low_memory=False)
df.to_csv(path, index=False, encoding='utf-8-sig', na_rep='')
raw = path.read_bytes()[:20]
print('BOM:', raw[:3])
print(df[['language', 'idioma_codigo', 'idioma_label']].drop_duplicates().head(6).to_dict(orient='records'))
