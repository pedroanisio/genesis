# Filename: list_directory_structure_atom.py
# Path: project_root/app/atoms/list_directory_structure_atom.py
# Log Level: INFO

import os
import logging
from datetime import datetime
from app.atoms.base_atom import BaseAtom

class ListDirectoryStructureAtom(BaseAtom):
    """
    Atom to list all files and directories in the specified directory,
    along with their attributes (size, modification time, etc.).
    """
    def __init__(self):
        super().__init__("ListDirectoryStructureAtom")

    def process(self, data: dict) -> dict:
        dir_name = data.get('dir_name')
        if not dir_name:
            raise ValueError('Directory name is required.')
        
        # Check if the directory exists
        if not os.path.exists(dir_name):
            raise FileNotFoundError(f'The directory "{dir_name}" does not exist.')

        structure = self._get_directory_structure(dir_name)
        logging.info(f'Directory structure for "{dir_name}" retrieved.')

        # Add the structure to the data dictionary
        data['directory_structure'] = structure
        return data

    def _get_directory_structure(self, dir_name):
        """
        Recursively lists all files and directories in the given directory,
        along with their attributes.
        """
        directory_structure = []

        for root, dirs, files in os.walk(dir_name):
            for name in dirs:
                dir_path = os.path.join(root, name)
                directory_structure.append(self._get_file_attributes(dir_path, is_directory=True))

            for name in files:
                file_path = os.path.join(root, name)
                directory_structure.append(self._get_file_attributes(file_path, is_directory=False))

        return directory_structure

    def _get_file_attributes(self, path, is_directory):
        """
        Get attributes for a file or directory.
        
        Args:
            path (str): Path to the file or directory.
            is_directory (bool): True if it's a directory, False if it's a file.
        
        Returns:
            dict: Dictionary with file or directory attributes.
        """
        attributes = {
            'path': path,
            'is_directory': is_directory,
            'size': os.path.getsize(path) if not is_directory else None,
            'last_modified': datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S'),
            'created': datetime.fromtimestamp(os.path.getctime(path)).strftime('%Y-%m-%d %H:%M:%S')
        }
        return attributes
