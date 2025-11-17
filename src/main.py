import time
from config import RSS_FEEDS, CHUNK_SIZE, RAW_PATH, AUDIO_PATH, JSON_FILENAME, NUMBER_OF_PODCAST_FOR_EACH_PODCAST
from utils import convert_mp3_to_wav, download_podcast_mp3, fetch_data, parse_data, sanitize_filename, save_data
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.Formatter.converter = time.gmtime 


def pipeline():
    logging.info("Starting podcast scraping pipeline")

    all_data = []
    for feed_url in RSS_FEEDS:
        logging.info(f"Processing feed: {feed_url}")
        # Fetching each feed 
        content = fetch_data(feed_url)

        if content:
            data_list = parse_data(content)
            logging.info(f"Found {len(data_list)} episodes in feed")
            all_data.extend(data_list)

            for episode in data_list[:NUMBER_OF_PODCAST_FOR_EACH_PODCAST]:
                logging.info(f"Processing episode: {episode['title']}")

                safe_filename = sanitize_filename(episode['title'])
                
                mp3_path = download_podcast_mp3(
                    episode['audio_url'], safe_filename, AUDIO_PATH, CHUNK_SIZE
                )

                if mp3_path:
                    wav_path = convert_mp3_to_wav(mp3_path)
                    episode['wav_path'] = wav_path  
        else:
            logging.warning(f"Failed to fetch content from {feed_url}")
    
    logging.info(f"Saving {len(all_data)} total episodes to JSON")
    save_data(all_data, JSON_FILENAME, RAW_PATH)
    logging.info("Pipeline completed successfully")

if __name__ == "__main__":
    pipeline()