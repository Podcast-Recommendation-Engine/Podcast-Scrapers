import json
import time
from config import ACKS, AUDIO_PATH, CHUNK_SIZE, KAFKA_URL, NUMBER_OF_PODCAST_FOR_EACH_PODCAST, PORT, RAW_PATH, RSS_FEEDS, TOPIC
from utils import  config, delivery_report, download_podcast_mp3, fetch_data, parse_data, sanitize_filename, save_data
import logging
from confluent_kafka import Producer


logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.Formatter.converter = time.gmtime  


def pipeline():
    logging.info("Starting podcast scraping pipeline")

    all_data = []
    config_value = config(url= KAFKA_URL, port= PORT, acks= ACKS)
    producer= Producer(config_value)

    for feed_url in RSS_FEEDS:

        logging.info(f"Processing feed: {feed_url}")
        content = fetch_data(feed_url)

        if not content:
            logging.warning(f"Failed to fetch content from {feed_url}")
            continue

        data_list = parse_data(content)
        logging.info(f"Found {len(data_list)} episodes in feed")
        
        all_data.extend(data_list)

        for episode in data_list[:NUMBER_OF_PODCAST_FOR_EACH_PODCAST]:
            logging.info(f"Processing episode: {episode['title']}")
            safe_filename = sanitize_filename(episode['title'])
            # full_path = download_podcast_mp3(episode['audio_url'], safe_filename, AUDIO_PATH, CHUNK_SIZE)
            # I only use this for testing the stt cause i have a small audio file called test.mp3
            full_path= "data/audio/test.mp3"

            logging.info(f"Saving {safe_filename}  episode to JSON")
            save_data(data= episode, filename= safe_filename.removesuffix(".mp3"), path= RAW_PATH)
            if full_path:
                logging.info(f"Sending to Kafka: {full_path}")
                producer.produce(
                    topic=TOPIC,
                    value=json.dumps(episode).encode('utf-8'), 
                    callback=delivery_report
                )

    producer.flush()
    logging.info("Pipeline completed successfully")

if __name__ == "__main__":
    pipeline()