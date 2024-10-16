# Filename: cinema_alchemist.py
# Path: project_root/recipes/cinema_alchemist.py
# Log Level: INFO

import logging  # Import the logging module to fix NameError

from app.atoms.list_mkv_files_atom import ListMkvFilesAtom
from app.atoms.sort_by_size_atom import SortBySizeAtom
from app.atoms.state_key_atom import StateKeyAtom
from app.atoms.state_check_atom import StateCheckAtom
from app.atoms.register_state_atom import RegisterStateAtom
from app.atoms.ffmpeg_atom import FfmpegAtom
from app.atoms.move_atom import MoveAtom
from app.atoms.rename_file_atom import RenameFileAtom
from app.atoms.final_state_update_atom import FinalStateUpdateAtom
from app.molecules.base_molecule import SequentialMolecule
from app.atoms.delete_file_atom import DeleteFileAtom

class CinemaAlchemist:
    """
    The Cinema Alchemist class that represents a sequence of atoms to process .mkv files.
    It encapsulates the entire processing logic in an object-oriented manner.
    """

    def __init__(self, mkv_dir, db_path, output_dir):
        """
        Initialize the Cinema Alchemist with the directory and database paths.
        Args:
            mkv_dir (str): The directory containing .mkv files.
            db_path (str): The path to the SQLite database for state storage.
            output_dir (str): The directory where processed files will be moved.
        """
        self.mkv_dir = mkv_dir
        self.db_path = db_path
        self.output_dir = output_dir
        self.molecule = SequentialMolecule()  # Use SequentialMolecule

        # Setup the processing chain (atoms) in the molecule
        self.setup_molecule()

    def setup_molecule(self):
        """Setup the molecule by adding the chain of atoms to it."""
        self.molecule.add_atom(ListMkvFilesAtom())            # Step 1: List files
        self.molecule.add_atom(SortBySizeAtom())              # Step 2: Sort by size
        # Atoms for each individual file will be added during processing

    def process(self, data: dict):
        """
        Execute the Cinema Alchemist processing chain.
        Args:
            data (dict): A dictionary containing any initial data.
        """
        # Step 1: Pass the directory name to ListMkvFilesAtom and SortBySizeAtom
        data['dir_name'] = self.mkv_dir
        data = self.molecule.run(data)  # Run List and Sort
       
        # Step 2: Loop through each file and process it individually
        for file_info in data.get('sorted_items', []):
            file_path = file_info['path']
            file_data = {'file_path': file_path}
            file_data['state_key'] = 'file_path' 

            try:
                # Set the file state to 'in-progress' before calling RegisterStateAtom
                file_data['state'] = 'in-progress'  # Fix: Add state key

                # Process each file using its own chain of atoms
                file_chain = SequentialMolecule()
                file_chain.add_atom(StateKeyAtom())  # Step 3: Set state key
                file_chain.add_atom(StateCheckAtom(self.db_path))   # Step 4: Check state
                file_chain.add_atom(RegisterStateAtom(self.db_path)) # Step 5: Register in-progress
                file_chain.add_atom(FfmpegAtom())                   # Step 6: Run ffmpeg
                file_chain.add_atom(DeleteFileAtom())      # Step 7: Delete original file              
                file_chain.add_atom(MoveAtom())      # Step 7: Move file
                file_chain.add_atom(RenameFileAtom('ffmpeg_processed_file','file_path'))                   # Step 8: Rename file
                file_chain.add_atom(FinalStateUpdateAtom(self.db_path)) # Step 9: Register completed state

                # Execute the file chain for this file
                file_chain.run(file_data)

            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}")
