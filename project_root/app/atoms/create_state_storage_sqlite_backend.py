import os
import sqlite3
import logging
from app.atoms.base_sqlite_atom import BaseSQLiteAtom

class CreateStateStorageSQLITEBackendAtom(BaseSQLiteAtom):
    """
    Atom to create and initialize an SQLite database for state storage.
    """
    
    def __init__(self, db_path):
        super().__init__("CreateStateStorageSQLITEBackendAtom", db_path)

    def process(self, data: dict) -> dict:
        # Check if the database already exists
        if not os.path.exists(self.db_path):
            try:
                # Create the SQLite database and the file_state table
                query = '''
                    CREATE TABLE IF NOT EXISTS file_state (
                        state_key TEXT PRIMARY KEY,
                        state TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                '''
                self.execute_query(query)
                logging.info(f"Created state storage at {self.db_path}")
            except sqlite3.Error as e:
                logging.error(f"Failed to create state storage at {self.db_path}: {e}")
                raise RuntimeError(f"Failed to initialize SQLite state storage: {e}")
        else:
            logging.info(f"State storage already exists at {self.db_path}")

        # Set a flag in the data to indicate successful initialization
        data['state_storage_initialized'] = True
        return data
