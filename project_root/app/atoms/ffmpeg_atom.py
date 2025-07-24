import subprocess
import logging
import threading
import itertools
import sys
import time
from app.atoms.base_atom import BaseAtom


class FfmpegAtom(BaseAtom):
    """
    Atom to run the ffmpeg command on the file to process it, with a spinner animation during execution.
    """
    
    def __init__(self):
        super().__init__("FfmpegAtom")
        self.output_dir =  '/mnt/local_buffer'

    def process(self, data: dict) -> dict:
        input_file = data.get('file_path')
        if not input_file:
            raise ValueError('Input file not provided for ffmpeg.')

        # Set the output file path (temporary output file with .temp extension)
        output_file = input_file
        # if the output directory is provided, use it
        if self.output_dir:
            output_file = f"{self.output_dir}/{input_file.split('/')[-1]}"

        # Define the ffmpeg command, explicitly specifying the format as 'matroska'
        ffmpeg_cmd = [
            'ffmpeg',
            '-loglevel', 'error',  # Reduce verbosity
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
        
        # Spinner thread to show progress while ffmpeg runs
        stop_spinner = threading.Event()
        spinner_thread = threading.Thread(target=self._spinner, args=(stop_spinner,))
        
        try:
            spinner_thread.start()  # Start the spinner animation
            # Execute the ffmpeg command
            subprocess.run(ffmpeg_cmd, check=True)
            stop_spinner.set()  # Stop the spinner after ffmpeg completes
            spinner_thread.join()
            logging.info(f"ffmpeg completed successfully for {input_file}")
            data['ffmpeg_processed_file'] = output_file
        except subprocess.CalledProcessError as e:
            stop_spinner.set()  # Ensure spinner stops in case of error
            spinner_thread.join()
            logging.error(f"ffmpeg failed for {input_file}: {e}")
            raise RuntimeError(f"ffmpeg failed for {input_file}")

        return data

    def _spinner(self, stop_event):
        """
        Spinner animation to show progress while the subprocess runs.
        """
        spinner = itertools.cycle(['|', '/', '-', '\\'])
        while not stop_event.is_set():
            sys.stdout.write(next(spinner))  # Print next spinner character
            sys.stdout.flush()  # Force write to console
            time.sleep(0.1)  # Control the speed of the spinner
            sys.stdout.write('\b')  # Backspace to overwrite the spinner
