# Filename: main.py
# Path: project_root/main.py
# Log Level: INFO

import logging
from app.atoms.create_state_storage_sqlite_backend import CreateStateStorageSQLITEBackendAtom
from app.recipes.cinema_alchemist import CinemaAlchemist

# Database and output directory paths
DB_PATH = './file_state.db'  # SQLite database for state storage
OUTPUT_DIR = './output'  # Output directory for processed files
MKV_DIR = '/mnt/local_media/movies'  # Directory containing .mkv files
LOG_FILE = './logs/process.log'  # Path to the log file

def main():
    """
    Main entry point for processing .mkv files using the Cinema Alchemist recipe.
    """
    # Configure logging to write to a file with the INFO level
    logging.basicConfig(
        level=logging.INFO,
        filename=LOG_FILE,  # Log file path
        filemode='a',  # Append to the log file ('w' for overwrite)
        format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format with timestamp
    )

    # Step 1: Initialize the SQLite state storage
    create_state_storage_atom = CreateStateStorageSQLITEBackendAtom(DB_PATH)
    data = {}
    create_state_storage_atom.process(data)

    # Step 2: Initialize the Cinema Alchemist class
    cinema_alchemist = CinemaAlchemist(MKV_DIR, DB_PATH, OUTPUT_DIR)

    # Step 3: Execute the Cinema Alchemist's processing chain
    cinema_alchemist.process(data)

if __name__ == "__main__":
    main()
