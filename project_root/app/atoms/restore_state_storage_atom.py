# Filename: restore_state_storage_atom.py
# Path: project_root/app/atoms/restore_state_storage_atom.py
# Log Level: INFO

import sqlite3
import logging
from app.atoms.base_sqlite_atom import BaseSQLiteAtom

class RestoreStateStorageAtom(BaseSQLiteAtom):
    """
    Atom to restore state from the SQLite database and load it into memory.
    """
    
    def __init__(self, db_path):
        super().__init__("RestoreStateStorageAtom", db_path)

    def process(self, data: dict) -> dict:
        # Execute query to retrieve all state data
        query = 'SELECT state_key, state FROM file_state'
        result = self.execute_query(query)

        # Load state into memory
        file_states = {row[0]: row[1] for row in result}
        logging.info(f"Restored state for {len(file_states)} files.")

        # Pass the loaded state to the next atom
        data['file_states'] = file_states
        return data
