
import os
from app.atoms.base_atom import BaseAtom

class DeleteFileAtom(BaseAtom):
    def __init__(self):
        super().__init__('DeleteFileAtom')

    def process(self, data: dict) -> dict:
        file_path = data.get('file_path')

        if not file_path:
            raise ValueError('No file path provided for deletion.')

        if os.path.exists(file_path):
            os.remove(file_path)
            data['file_deleted'] = True
        else:
            data['file_deleted'] = False
        
        return data

