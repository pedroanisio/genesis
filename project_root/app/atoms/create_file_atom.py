# Filename: create_file_atom.py
# Path: project_root/app/atoms/create_file_atom.py
# Log Level: INFO

import os
import logging  # Ensure the logging module is imported
from app.atoms.base_atom import BaseAtom

class CreateFileAtom(BaseAtom):
    """
    Atom to create a file with content inside the specified directory.
    """
    def __init__(self):
        super().__init__("CreateFileAtom")

    def process(self, data: dict) -> dict:
        dir_name = data.get('dir_name', '.')
        file_name = data.get('file_name')
        content = data.get('content', '')

        if not file_name:
            raise ValueError('File name is required.')
        
        file_path = os.path.join(dir_name, file_name)
        with open(file_path, 'w') as file:
            file.write(content)
        
        logging.info(f'File "{file_name}" created in directory "{dir_name}".')
        
        data['status'] = f'File "{file_name}" created.'
        return data
