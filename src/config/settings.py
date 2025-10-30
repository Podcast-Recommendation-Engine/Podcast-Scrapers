import os
from models.podcast import Podcast

RSS_FEEDS = [
    Podcast('lex-fridman', 'https://lexfridman.com/feed/podcast/'),
    Podcast('joe-rogan', 'https://feeds.megaphone.fm/GLT1412515089'),
]

SAVE_DIRECTORY = os.getenv('DOWNLOAD_DIR', '../downloads')
MAX_EPISODES_PER_FEED = 1
DOWNLOAD_RETRIES = 3
SLEEP_TIME = 1
CONVERT_TO_WAV = True
