# Filename: move_atom.py
# Path: project_root/app/atoms/move_atom.py
# Log Level: INFO

import os
import shutil
import logging
from app.atoms.base_atom import BaseAtom

class MoveAtom(BaseAtom):
    """
    Atom to move the processed file to the output directory.
    """
    def __init__(self, output_dir):
        super().__init__("MoveAtom")
        self.output_dir = output_dir

    def process(self, data: dict) -> dict:
        processed_file = data.get('processed_file')
        ffmpeg_processed_file = data.get('ffmpeg_processed_file')
        if not processed_file:
            raise ValueError('Processed file not provided for moving.')

        shutil.move(ffmpeg_processed_file, processed_file)
        logging.info(f"Moved file to {processed_file}")
        data['moved_file'] = processed_file
        return data
