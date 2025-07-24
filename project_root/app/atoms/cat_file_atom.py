# Filename: cat_file_atom.py
# Path: project_root/app/atoms/cat_file_atom.py
# Log Level: INFO

import logging
from app.atoms.base_atom import BaseAtom

class CatFileAtom(BaseAtom):
    """
    Atom to simulate the 'cat' command: read and print the content of files.
    """

    def __init__(self):
        super().__init__("CatFileAtom")

    def process(self, data: dict) -> dict:
        directory_structure = data.get('directory_structure', [])
        if not directory_structure:
            raise ValueError('No directory structure found to process.')

        for item in directory_structure:
            if not item['is_directory']:
                file_path = item['path']
                logging.info(f'Catting file: {file_path}')
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        print(f'--- Content of {file_path} ---\n{content}\n')
                except Exception as e:
                    logging.error(f'Failed to read file {file_path}: {e}')

        return data
