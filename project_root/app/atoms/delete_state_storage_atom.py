# Filename: delete_state_storage_atom.py
# Path: project_root/app/atoms/delete_state_storage_atom.py
# Log Level: INFO

import sqlite3
import logging
import os
from app.atoms.base_atom import BaseAtom

class DeleteStateStorageAtom(BaseAtom):
    """
    Atom to delete or reset the state storage.
    """
    def __init__(self, db_path, reset_table=False):
        super().__init__("DeleteStateStorageAtom")
        self.db_path = db_path
        self.reset_table = reset_table

    def process(self, data: dict) -> dict:
        if self.reset_table:
            # Reset the table but keep the database file
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM file_state')
            conn.commit()
            conn.close()
            logging.info(f"State table reset in {self.db_path}")
        else:
            # Delete the SQLite database file
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
                logging.info(f"Deleted state storage at {self.db_path}")
            else:
                logging.info(f"No state storage found at {self.db_path}")

        return data
