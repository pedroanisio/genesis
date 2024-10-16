# Filename: create_directory_atom.py
# Path: project_root/app/atoms/create_directory_atom.py
# Log Level: INFO

import os
import logging  # Ensure the logging module is imported
from app.atoms.base_atom import BaseAtom

class CreateDirectoryAtom(BaseAtom):
    """
    Atom to create a directory if it does not exist.
    """
    def __init__(self):
        super().__init__("CreateDirectoryAtom")

    def process(self, data: dict) -> dict:
        dir_name = data.get('dir_name')
        if not dir_name:
            raise ValueError('Directory name is required.')
        
        os.makedirs(dir_name, exist_ok=True)
        logging.info(f'Directory "{dir_name}" created or already exists.')
        
        data['status'] = f'Directory "{dir_name}" ensured.'
        return data
