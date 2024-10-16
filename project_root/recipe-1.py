# Filename: main.py
# Path: project_root/main.py
# Log Level: INFO

import logging
import os
from app.atoms.list_mkv_files_atom import ListMkvFilesAtom
from app.molecules.base_molecule import SequentialMolecule

def main():
    """
    Example of building and running a sequential molecule to list all .mkv files
    in a specified directory and print their attributes.
    """
    # Directory to search for .mkv files (you can change this to the desired directory)
    dir_name = os.path.expanduser('/mnt/media/movies')  # Example: User's Videos folder

    # Initial data with the directory name
    data = {
        'dir_name': dir_name,
    }

    # Build molecule to list .mkv files and their attributes
    molecule = SequentialMolecule()
    molecule.add_atom(ListMkvFilesAtom())

    # Execute molecule
    try:
        result = molecule.run(data)
        # Print the found .mkv files and their attributes
        mkv_files = result.get('mkv_files', [])
        for file_info in mkv_files:
            print(file_info)
    except Exception as e:
        print(f'Execution failed: {e}')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
