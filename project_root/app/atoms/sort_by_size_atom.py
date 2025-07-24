
from app.atoms.base_atom import BaseAtom

class SortBySizeAtom(BaseAtom):
    def __init__(self):
        super().__init__('SortBySizeAtom')

    def process(self, data: dict) -> dict:
        items = data.get('items', [])
        sorted_items = sorted(items, key=lambda x: x.get('size', 0), reverse=True)
        data['sorted_items'] = sorted_items
        return data

