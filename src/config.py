import os
from dotenv import load_dotenv
load_dotenv()

RSS_FEEDS = [
    "https://lexfridman.com/feed/podcast/",
    # "https://feeds.megaphone.fm/GLT1412515089"
]
CHUNK_SIZE = 8192
RAW_PATH = "data/raw"
AUDIO_PATH = "data/audio"
JSON_FILENAME = "podcasts.json"
NUMBER_OF_PODCAST_FOR_EACH_PODCAST= 2


KAFKA_URL= os.getenv('KAFKA_URL', 'kafka')
PORT = int(os.getenv('PORT', '9092'))
ACKS = int(os.getenv('ACKS', 1))
TOPIC= os.getenv('AUDIO_TOPIC', 'podcast_audio')