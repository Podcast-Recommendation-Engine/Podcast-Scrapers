import os
from dotenv import load_dotenv
load_dotenv()

RSS_FEEDS = [
    "https://lexfridman.com/feed/podcast/",
    "https://feeds.megaphone.fm/GLT1412515089",
    "https://feeds.simplecast.com/qm_9xx0g",
    "https://feeds.simplecast.com/54nAGcIl",
    "https://feeds.simplecast.com/mKn_QmLS",
    "https://feeds.megaphone.fm/thispastweekend",
    "https://podcastfeeds.nbcnews.com/HL4TzgYC",
    "https://www.thisamericanlife.org/podcast/rss.xml",
    "https://feeds.simplecast.com/6Qp23t6h",
    "https://feeds.simplecast.com/hNaFxXpO",
    "https://rss.art19.com/new-heights",

]
CHUNK_SIZE = 8192
RAW_PATH = "data/bronze/metadata"
AUDIO_PATH = "data/bronze/audio"
NUMBER_OF_PODCAST_FOR_EACH_PODCAST= 3


KAFKA_URL= os.getenv('PS_KAFKA_URL', 'kafka')
PORT = int(os.getenv('PS_KAFKA_PORT', '9092'))
ACKS = int(os.getenv('PS_KAFKA_ACKS', 1))
TOPIC= os.getenv('PS_KAFKA_TOPIC_OUT', 'podcast_audio')