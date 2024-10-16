import os
import logging
from app.atoms.base_atom import BaseAtom

class DeleteFileAtom(BaseAtom):
    """
    Atom to delete a file from the file system.
    """
    
    def __init__(self):
        super().__init__("DeleteFileAtom")

    def process(self, data: dict) -> dict:
        file_path = data.get('file_path')

        if not file_path:
            raise ValueError('No file path provided for deletion.')

        try:
            # Check if the file exists
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"File '{file_path}' deleted successfully.")
                data['file_deleted'] = True
            else:
                logging.warning(f"File '{file_path}' does not exist. Nothing to delete.")
                data['file_deleted'] = False
        except Exception as e:
            logging.error(f"Failed to delete file '{file_path}': {e}")
            raise RuntimeError(f"Failed to delete file '{file_path}'")

        return data
