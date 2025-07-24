# Filename: register_state_atom.py
# Path: project_root/app/atoms/register_state_atom.py
# Log Level: INFO

import logging
from app.atoms.base_sqlite_atom import BaseSQLiteAtom

class RegisterStateAtom(BaseSQLiteAtom):
    """
    Atom to register or update the state of a file in the state store (SQLite).
    """
    
    def __init__(self, db_path):
        super().__init__("RegisterStateAtom", db_path)

    def process(self, data: dict) -> dict:
        state_key = data.get('state_key')
        state = data.get('state')

        if not state_key or not state:
            raise ValueError('State key or state not provided for registration.')

        # Execute the query to insert or update the file state
        query = '''
            INSERT INTO file_state (state_key, state)
            VALUES (?, ?)
            ON CONFLICT(state_key) DO UPDATE 
            SET state = excluded.state, timestamp = CURRENT_TIMESTAMP
        '''
        self.execute_query(query, (state_key, state))

        logging.info(f"State updated for '{state_key}' to '{state}'.")
        return data
