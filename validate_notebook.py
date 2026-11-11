import json
from pathlib import Path

p = Path('notebooks/03_Modelo.ipynb')
data = json.loads(p.read_text(encoding='utf-8'))
flags = ['\\Users', 'tmp_', 'validate_notebook', 'revert', 'reset']
for i, cell in enumerate(data['cells']):
    if cell.get('cell_type') == 'code':
        src = ''.join(cell.get('source', []))
        hits = [f for f in flags if f in src or f in src.lower()]
        if hits:
            print(f'CELL {i}: {hits}')
            print(src[:600])
            print('---')
