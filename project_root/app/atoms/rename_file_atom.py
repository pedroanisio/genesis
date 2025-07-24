import os
import logging
from app.atoms.base_atom import BaseAtom

class RenameFileAtom(BaseAtom):
    """
    Atom to rename a file. It can receive 'from_path' (original file path) and 'to_path' (new file path)
    either in the constructor or from the 'data' dictionary during processing.
    """
    
    def __init__(self, from_path_key: str = None, to_path_key: str = None):
        """
        Initialize the RenameFileAtom with optional 'from_path_key' and 'to_path_key'.
        
        Args:
            from_path_key (str): Key in the data dict for the original file path to be renamed (optional).
            to_path_key (str): Key in the data dict for the new file path or new name (optional).
        """
        super().__init__("RenameFileAtom")
        self.from_path_key = from_path_key
        self.to_path_key = to_path_key

    def process(self, data: dict) -> dict:
        """
        Renames the file using the 'from_path' and 'to_path' provided either in the constructor 
        or from the 'data' dictionary.
        
        Args:
            data (dict): Should contain 'from_path' (the current file path) and 'to_path' 
                         (the new file name) if not provided in constructor.
                         
        Returns:
            dict: Updated data dictionary with the 'renamed_file' key added.
        """
        # Fetch paths from instance variables or the data dictionary
        from_path = data.get(self.from_path_key) if self.from_path_key else data.get('from_path')
        to_path = data.get(self.to_path_key) if self.to_path_key else data.get('to_path')

        # Validate the paths
        if not from_path or not to_path:
            logging.error('Both "from_path" and "to_path" are required for renaming.')
            raise ValueError('Both "from_path" and "to_path" are required for renaming.')

        try:
            # Attempt to rename the file
            os.rename(from_path, to_path)
            logging.info(f"Successfully renamed file from '{from_path}' to '{to_path}'")
            data['renamed_file'] = to_path  # Update the data with the new file path

        except FileNotFoundError:
            logging.error(f"File '{from_path}' not found. Cannot rename.")
            raise RuntimeError(f"File '{from_path}' not found. Renaming failed.")
        except PermissionError:
            logging.error(f"Permission denied when trying to rename '{from_path}' to '{to_path}'.")
            raise RuntimeError(f"Permission denied when renaming '{from_path}' to '{to_path}'.")
        except Exception as e:
            logging.error(f"An unexpected error occurred while renaming '{from_path}' to '{to_path}': {e}")
            raise RuntimeError(f"Renaming failed for '{from_path}' due to an unexpected error: {e}")

        return data
