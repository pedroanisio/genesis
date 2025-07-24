
import os
from app.atoms.base_atom import BaseAtom

class ListMkvFilesAtom(BaseAtom):
    def __init__(self):
        super().__init__('ListMkvFilesAtom')

    def process(self, data: dict) -> dict:
        dir_name = data.get('dir_name')
        if not dir_name:
            raise ValueError('Directory name is required.')
        
        mkv_files = []
        for root, dirs, files in os.walk(dir_name):
            for file_name in files:
                if file_name.endswith('.mkv'):
                    mkv_files.append({'filename': file_name, 'path': os.path.join(root, file_name)})
        
        data['items'] = mkv_files
        return data

