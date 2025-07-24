
import os
from app.atoms.base_atom import BaseAtom

class CreateDirectoryAtom(BaseAtom):
    def __init__(self):
        super().__init__('CreateDirectoryAtom')

    def process(self, data: dict) -> dict:
        dir_name = data.get('dir_name')
        if not dir_name:
            raise ValueError('Directory name is required.')
        
        os.makedirs(dir_name, exist_ok=True)
        data['status'] = f'Directory {dir_name} ensured.'
        return data

