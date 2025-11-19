import json
import os
import re
import time
import uuid
import feedparser
import requests
from pydub import AudioSegment
import logging


logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.Formatter.converter = time.gmtime 

def fetch_data(feed: str):
    try:
        conn = requests.get(feed, timeout=10)
        if conn.status_code != 200:
            logging.warning(f"Failed to fetch data from {feed} (status code: {conn.status_code})")
            return None
        
        return conn.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None


def parse_data(content: str):
    parsed_data = []
    data = feedparser.parse(content)

    for entry in data.entries:

        published_parsed = entry.get('published_parsed')
        year = month = day = hour = minute = second = weekday = yearday = is_dst = None
        if published_parsed:
            year, month, day, hour, minute, second, weekday, yearday, is_dst = published_parsed


        audio_url = next(
            (link.get('href') for link in entry.get('links') or [] if link.get('rel') == "enclosure"),
            None
        )
        duration = entry.get('itunes_duration', 'N/A')
        if ':' in duration:
            duration= determine_duration_in_seconds(duration=duration) 

        episode = {
        'id':  generate_uuid(),
        'title': entry.get('title'),
        # 'links': entry.get('links'),
        'audio_url': audio_url,
        'year': year,
        'month': month,
        'day': day,
        'hour': hour,
        'minute': minute,
        'second': second,
        'weekday': weekday,
        'yearday': yearday,
        'is_dst': is_dst,
        # 'summary': entry.get('summary'),
        # 'content': entry.get('content'),
        'subtitle': entry.get('subtitle'),
        'authors': entry.get('authors'),
        'image': entry.get('image'),
        'itunes_duration': duration,
        'wav_path': None
        }

        parsed_data.append(episode)
    return parsed_data

 
def save_data(data: list, filename: str, path: str):
    os.makedirs(path, exist_ok=True)
    full_path = os.path.join(path, filename)
    with open(full_path, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    


def download_podcast_mp3(url: str, filename: str, path: str, chunk_size: int = 8192):
    try:
        os.makedirs(path, exist_ok=True)
        full_path = os.path.join(path, filename)
        
        # Skip if already downloaded
        # if os.path.exists(full_path):
        #     logging.info(f"File already exists, skipping: {full_path}")
        #     return full_path
        
        response = requests.get(url, stream=True, timeout=30)
        if response.status_code != 200:
            logging.warning(f"Failed to download: {url} (status code: {response.status_code})")
            return None

        with open(full_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
        logging.info(f"Downloaded: {full_path}")
        return full_path

    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading file: {e}")
        return None
    

def sanitize_filename(filename: str) -> str:
    # Remove invalid characters for Windows filenames
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace multiple spaces with single space
    filename = re.sub(r'\s+', ' ', filename)
    # Trim and add .mp3 extension if not present
    filename = filename.strip()
    if not filename.endswith('.mp3'):
        filename += '.mp3'
    return filename


def generate_uuid()-> str:
    return str(uuid.uuid4())

def determine_duration_in_seconds(duration: str) -> float:

    parts = list(map(int, duration.split(":")))
    
    if len(parts) == 3:      # HH:MM:SS
        h, m, s = parts

    # MM:SS
    else:
        h = 0
        m, s = parts

    return h * 3600 + m * 60 + s 


# def convert_mp3_to_wav(mp3_path: str, delete_mp3: bool = True):
#     try:
#         wav_path = os.path.splitext(mp3_path)[0] + '.wav'
#         audio = AudioSegment.from_mp3(mp3_path)
#         audio = audio.set_channels(1)
#         audio = audio.set_frame_rate(16000)
#         audio = audio.set_sample_width(2)
#         audio.export(wav_path, format='wav')

#         logging.info(f"Converted: {mp3_path} -> {wav_path}")
        
#         # Cleanup MP3 after successful conversion
#         # if delete_mp3:
#         #     os.remove(mp3_path)
#         #     logging.info(f"Removed original MP3: {mp3_path}")
        
#         return wav_path

#     except Exception as e:
#         logging.error(f"Error converting file: {e}")
        # return None
