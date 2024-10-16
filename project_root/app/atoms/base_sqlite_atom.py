import sqlite3
import logging
from abc import ABC, abstractmethod
from app.atoms.base_atom import BaseAtom

class BaseSQLiteAtom(BaseAtom, ABC):
    """
    Base class for SQLite-based atoms that encapsulates common database operations
    and error handling.
    """

    def __init__(self, name: str, db_path: str):
        super().__init__(name)
        self.db_path = db_path

    @abstractmethod
    def process(self, data: dict) -> dict:
        """
        The specific atom's logic will be implemented in subclasses.
        """
        pass

    def execute_query(self, query: str, params: tuple = ()):
        """
        Executes a given SQL query and handles database connection and exceptions.

        Args:
            query (str): The SQL query to execute.
            params (tuple): Optional parameters for the query.

        Returns:
            list: Query result for SELECT queries or None for non-SELECT queries.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                
                if query.strip().upper().startswith("SELECT"):
                    result = cursor.fetchall()  # Fetch data if it's a SELECT query
                    logging.info(f"Query executed successfully: {query}")
                    return result
                else:
                    conn.commit()  # Commit changes for UPDATE/INSERT/DELETE
                    logging.info(f"Database updated successfully with query: {query}")
        except sqlite3.Error as e:
            logging.error(f"SQLite error: {e} - Query: {query}")
            raise RuntimeError(f"Database error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e} - Query: {query}")
            raise RuntimeError(f"Unexpected error: {e}")

        return None
