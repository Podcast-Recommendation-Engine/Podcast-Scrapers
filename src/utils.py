import json
import os
import re
import time
import uuid
import feedparser
import requests
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
        if isinstance(duration, str) and ':' in duration:
            duration = determine_duration_in_seconds(duration)

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
    # HH:MM:SS
    if len(parts) == 3:      
        h, m, s = parts

    # MM:SS
    else:
        h = 0
        m, s = parts

    return h * 3600 + m * 60 + s 

# Kafka establish connection using this function
def config(url: str, port: int, acks: int):
    config_dict = {
        "bootstrap.servers": f"{url}:{port}",
        "acks": acks
    }
    return config_dict 

def delivery_report(err, msg):
    if err :
        logging.error(f"Delivery Failed: {err}")
        return
    logging.info(f"Delivered message to {msg.topic()} [{msg.partition()}]")


