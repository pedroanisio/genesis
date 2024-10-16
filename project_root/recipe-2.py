# Filename: main.py
# Path: project_root/main.py
# Log Level: INFO

import logging
import os
from app.atoms.list_mkv_files_atom import ListMkvFilesAtom
from app.atoms.sort_by_size_atom import SortBySizeAtom
from app.molecules.base_molecule import SequentialMolecule

def main():
    """
    Example of building and running a sequential molecule to list all .mkv files
    in a specified directory and sort them by size in descending order.
    """
    # Directory to search for .mkv files
    dir_name = os.path.expanduser('/mnt/media/movies')  # Example: User's Videos folder

    # Initial data with the directory name
    data = {
        'dir_name': dir_name,
    }

    # Build molecule to list .mkv files and sort them by size
    molecule = SequentialMolecule()
    molecule.add_atom(ListMkvFilesAtom())  # List all .mkv files
    molecule.add_atom(SortBySizeAtom())    # Sort the list by size

    # Execute molecule
    try:
        result = molecule.run(data)
        # Print the sorted .mkv files
        sorted_mkv_files = result.get('sorted_items', [])
        for file_info in sorted_mkv_files:
            print(file_info)
    except Exception as e:
        print(f'Execution failed: {e}')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
