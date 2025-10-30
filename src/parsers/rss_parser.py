import requests
import feedparser
import logging
import os
import time
from urllib.parse import urlparse, unquote
from util.file_utils import sanitize_title
from util.audio_converter import convert_to_wav
from downloader.audio_downloader import download_file

def fetch_rss_feed(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException:
        return None

def parse_and_download(content, save_dir, retries=3, sleep_time=1, max_episodes=None, convert_to_wav_flag=False):
    feed = feedparser.parse(content)
    total_available = sum(1 for entry in feed.entries if any(link.type == 'audio/mpeg' for link in entry.get('links', [])))
    total_audio_files = min(total_available, max_episodes) if max_episodes else total_available
    
    logging.info(f"Available: {total_available}, Downloading: {total_audio_files}")
    
    audio_file_counter = 0
    successful_downloads = 0
    
    for entry in feed.entries:
        if max_episodes and audio_file_counter >= max_episodes:
            break
            
        if 'links' in entry:
            for link in entry.links:
                if link.type == 'audio/mpeg':
                    audio_file_counter += 1
                    title = sanitize_title(entry.title, entry.get('published'))
                    parsed_url = urlparse(unquote(link.href))
                    _, file_extension = os.path.splitext(parsed_url.path)
                    filename = os.path.join(save_dir, title + file_extension)

                    if download_file(link.href, filename, retries):
                        successful_downloads += 1
                        if convert_to_wav_flag:
                            convert_to_wav(filename)
                    
                    if max_episodes and audio_file_counter >= max_episodes:
                        break
                    
                    time.sleep(sleep_time)
    
    return successful_downloads, total_audio_files
