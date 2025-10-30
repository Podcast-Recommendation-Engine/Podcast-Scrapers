import subprocess
import os
import logging

def convert_to_wav(input_file):
    output_file = os.path.splitext(input_file)[0] + '.wav'
    
    try:
        subprocess.run(
            ['ffmpeg', '-i', input_file, '-acodec', 'pcm_s16le', '-ar', '44100', output_file, '-y'],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        os.remove(input_file)
        logging.info(f"Converted to WAV: {output_file}")
        return output_file
    except subprocess.CalledProcessError:
        logging.error(f"Failed to convert: {input_file}")
        return input_file
    except Exception as e:
        logging.error(f"Error: {e}")
        return input_file
