import pandas as pd
from pathlib import Path

raw = Path('c:/Users/admin/Documents/GitHub/visualizacion-de-datos-StreamView-Analytics/data/raw')
files = sorted(raw.glob('*.csv'))
print('FILES', [f.name for f in files])
for f in files:
    df = pd.read_csv(f, nrows=2)
    print('\nFILE', f.name)
    print(df.columns.tolist())
    print(df.head(1).to_dict(orient='records')[0])
