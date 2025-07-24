
import os
from app.atoms.base_atom import BaseAtom

class CreateFileAtom(BaseAtom):
    def __init__(self):
        super().__init__('CreateFileAtom')

    def process(self, data: dict) -> dict:
        dir_name = data.get('dir_name', '.')
        file_name = data.get('file_name')
        content = data.get('content', '')

        if not file_name:
            raise ValueError('File name is required.')
        
        file_path = os.path.join(dir_name, file_name)
        with open(file_path, 'w') as file:
            file.write(content)
        
        data['status'] = f'File {file_name} created.'
        return data

