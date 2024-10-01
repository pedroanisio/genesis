# Filename: ffmpeg_atom.py
# Path: project_root/app/atoms/ffmpeg_atom.py
# Log Level: INFO

import subprocess
import logging
from app.atoms.base_atom import BaseAtom

class FfmpegAtom(BaseAtom):
    """
    Atom to run the ffmpeg command on the file to process it.
    """
    def __init__(self):
        super().__init__("FfmpegAtom")

    def process(self, data: dict) -> dict:
        input_file = data.get('file_path')
        if not input_file:
            raise ValueError('Input file not provided for ffmpeg.')

        # Set the output file path (temporary output file with .temp extension)
        output_file = input_file + '.temp'

        # Define the ffmpeg command, explicitly specifying the format as 'matroska'
        ffmpeg_cmd = [
            'ffmpeg',
            '-loglevel', 'error',  # Add this line to reduce verbosity
            '-c:v', 'hevc',  # Input video codec
            '-i', input_file,  # Input file
            '-vf', 'format=p010le',  # Video filter
            '-c:v', 'hevc_nvenc',  # Output video codec (NVIDIA hardware encoding)
            '-preset', 'fast',  # Preset for speed/quality tradeoff
            '-b:v', '15M',  # Video bitrate
            '-c:a', 'copy',  # Audio codec (copy the original)
            '-f', 'matroska',  # Force the output format to Matroska (MKV)
            output_file  # Output file
        ]

        logging.info(f"Running ffmpeg on {input_file} with output to {output_file}")
        
        try:
            # Execute the ffmpeg command
            subprocess.run(ffmpeg_cmd, check=True)
            logging.info(f"ffmpeg completed successfully for {input_file}")
            data['processed_file'] = output_file
        except subprocess.CalledProcessError as e:
            logging.error(f"ffmpeg failed for {input_file}: {e}")
            raise RuntimeError(f"ffmpeg failed for {input_file}")

        return data
