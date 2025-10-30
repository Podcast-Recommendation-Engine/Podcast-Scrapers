import os
import logging
from config import RSS_FEEDS, SAVE_DIRECTORY, DOWNLOAD_RETRIES, SLEEP_TIME, MAX_EPISODES_PER_FEED
from parsers import fetch_rss_feed, parse_and_download

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    if not RSS_FEEDS:
        logging.error("No RSS feeds configured")
        return
    
    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)
    
    total_successful = 0
    total_files = 0
    
    for idx, podcast in enumerate(RSS_FEEDS, 1):
        logging.info(f"\nProcessing {idx}/{len(RSS_FEEDS)}: {podcast.name}")
        
        content = fetch_rss_feed(podcast.url)
        if content:
            successful, total = parse_and_download(content, SAVE_DIRECTORY, DOWNLOAD_RETRIES, SLEEP_TIME, MAX_EPISODES_PER_FEED)
            total_successful += successful
            total_files += total
            logging.info(f"Completed: {successful}/{total} files\n")
        else:
            logging.error(f"Failed to fetch: {podcast.name}\n")
    
    logging.info(f"\nTotal: {total_successful}/{total_files} files downloaded\n")

if __name__ == "__main__":
    main()
