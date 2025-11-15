import subprocess
import os
import logging

def convert_to_wav(input_file):
    """
    Convert audio file to WAV format optimized for podcast transcription
    - 16kHz sample rate (STT standard)
    - Mono audio (single channel)
    - 16-bit PCM encoding
    """
    output_file = os.path.splitext(input_file)[0] + '.wav'
    
    try:
        subprocess.run(
            [
                'ffmpeg', 
                '-i', input_file, 
                '-acodec', 'pcm_s16le',  # 16-bit PCM
                '-ar', '16000',           # 16kHz sample rate (changed from 44100)
                '-ac', '1',               # Mono (added - single channel)
                '-y',                     # Overwrite (moved before output)
                output_file
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        os.remove(input_file)
        
        # Log file size for verification
        size_mb = os.path.getsize(output_file) / (1024**2)
        logging.info(f"Converted to WAV (16kHz mono): {output_file} ({size_mb:.1f} MB)")
        
        return output_file
    except subprocess.CalledProcessError:
        logging.error(f"Failed to convert: {input_file}")
        return input_file
    except Exception as e:
        logging.error(f"Error: {e}")
        return input_file