# Filename: list_mkv_files_atom.py
# Path: project_root/app/atoms/list_mkv_files_atom.py
# Log Level: INFO

import os
import logging
from datetime import datetime
from stat import filemode
from app.atoms.base_atom import BaseAtom

class ListMkvFilesAtom(BaseAtom):
    """
    Atom to list all .mkv files in a folder recursively, along with
    their attributes: filename, access time, creation time, permissions, and size.
    input dict: dir_name (str) - The directory to search for .mkv files.
    """
    def __init__(self):
        super().__init__("ListMkvFilesAtom")

    def process(self, data: dict) -> dict:
        dir_name = data.get('dir_name')
        if not dir_name:
            raise ValueError('Directory name is required.')
        
        if not os.path.exists(dir_name):
            raise FileNotFoundError(f'The directory "{dir_name}" does not exist.')

        # Get list of .mkv files and their attributes
        mkv_files = self._get_mkv_files(dir_name)
        logging.info(f'Found {len(mkv_files)} .mkv files in "{dir_name}".')

        # Place the mkv files list in the data dictionary under the key 'items'
        data['items'] = mkv_files
        return data

    def _get_mkv_files(self, dir_name):
        """
        Recursively lists all .mkv files in the directory and their attributes.
        """
        mkv_files = []

        for root, dirs, files in os.walk(dir_name):
            for file_name in files:
                if file_name.endswith('.mkv'):
                    file_path = os.path.join(root, file_name)
                    mkv_files.append(self._get_file_attributes(file_path))

        return mkv_files

    def _get_file_attributes(self, file_path):
        """
        Get attributes for a .mkv file.
        
        Args:
            file_path (str): Path to the file.
        
        Returns:
            dict: Dictionary with file attributes (filename, atime, ctime, permissions, size).
        """
        stats = os.stat(file_path)
        attributes = {
            'filename': os.path.basename(file_path),
            'path': file_path,
            'size': stats.st_size,
            'atime': datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
            'ctime': datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'permissions': filemode(stats.st_mode)
        }
        return attributes
