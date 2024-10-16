import sqlite3
import logging
from app.atoms.base_sqlite_atom import BaseSQLiteAtom

class StateCheckAtom(BaseSQLiteAtom):
    """
    Atom to check if a file has already been processed by looking up the state using the state key.
    """
    
    def __init__(self, db_path):
        super().__init__("StateCheckAtom", db_path)

    def process(self, data: dict) -> dict:
        state_key = data.get('state_key')
        if not state_key:
            raise ValueError('No state key provided for state check.')

        # Execute query to check the state of the file
        query = 'SELECT state FROM file_state WHERE state_key = ?'
        result = self.execute_query(query, (state_key,))

        if result and result[0][0] == 'completed':
            logging.info(f"File '{state_key}' has already been processed. Skipping.")
            data['skip'] = True  # Mark the file to be skipped
        else:
            logging.info(f"File '{state_key}' has not been processed. Proceeding.")
            data['skip'] = False

        return data
