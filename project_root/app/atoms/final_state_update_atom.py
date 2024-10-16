import sqlite3
import logging
from app.atoms.base_sqlite_atom import BaseSQLiteAtom

class FinalStateUpdateAtom(BaseSQLiteAtom):
    """
    Atom to mark the file as 'completed' in the state store.
    """
    
    def __init__(self, db_path):
        super().__init__("FinalStateUpdateAtom", db_path)

    def process(self, data: dict) -> dict:
        state_key = data.get('state_key')
        if not state_key:
            raise ValueError('State key not provided for final state update.')

        # Execute query to update the state of the file
        query = '''
            UPDATE file_state
            SET state = 'completed', timestamp = CURRENT_TIMESTAMP
            WHERE state_key = ?
        '''
        self.execute_query(query, (state_key,))
        
        logging.info(f"File '{state_key}' marked as completed.")
        return data
