# Podcast-Scrapers

## Overview

This repository is dedicated to developing and managing a set of **podcast scrapers** that extract podcast audio files from **RSS feeds**.  
The goal is to **download and organize** podcast episodes with sanitized filenames to feed into the **Podcast Recommendation Platform**.

The scraper is modular, reliable, and uses a configuration-based approach for managing multiple RSS feeds.

---

## Features

- Downloads audio files from multiple RSS feeds specified in configuration
- Support for named podcasts using Podcast model (name + URL)
- Configurable episode limit per feed (avoid downloading thousands of episodes)
- Sanitizes episode titles to create filesystem-friendly filenames
- Automatic retry logic with exponential backoff for failed downloads
- Date-prefixed filenames (YYYY-MM-DD format)
- Modular architecture with separated concerns (config, parsing, downloading, utilities)
- Configurable download parameters (retries, sleep time, save directory, max episodes)
- Comprehensive logging for monitoring download progress

---

## Project Structure

```
src/
├── main.py                 # Main entry point
├── config/                 # Configuration settings
│   ├── __init__.py
│   └── settings.py         # RSS feeds and download parameters
├── downloader/             # Download logic
│   ├── __init__.py
│   └── audio_downloader.py # Audio file downloader with retry
├── parsers/                # RSS feed parsing
│   ├── __init__.py
│   └── rss_parser.py       # RSS feed fetcher and parser
├── util/                   # Utility functions
│   ├── __init__.py
│   └── file_utils.py       # File name sanitization
└── models/                 # Data models
    ├── __init__.py
    └── podcast.py          # Podcast model (name + URL)
```

---

## Configuration

Edit `src/config/settings.py` to configure your RSS feeds and download settings:

```python
from models.podcast import Podcast

# RSS Feed URLs to scrape - Format: Podcast(name, url)
RSS_FEEDS = [
    Podcast('lex-fridman', 'https://lexfridman.com/feed/podcast/'),
    Podcast('joe-rogan', 'https://feeds.megaphone.fm/GLT1412515089'),
    # Add more podcasts here
]

# Directory to save downloaded files
SAVE_DIRECTORY = "downloads"

# Maximum number of episodes to download per feed (None = download all)
MAX_EPISODES_PER_FEED = 10

# Number of retry attempts for failed downloads
DOWNLOAD_RETRIES = 3

# Sleep time between downloads (in seconds)
SLEEP_TIME = 1
```

---

## Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure RSS feeds:**
   - Open `src/config/settings.py`
   - Add your RSS feed URLs to the `RSS_FEEDS` list

3. **Run the scraper:**
   ```bash
   cd src
   python main.py
   ```

The scraper will:
- Create the download directory if it doesn't exist
- Process each RSS feed sequentially
- Download all audio files with sanitized, date-prefixed filenames
- Provide detailed logging of the download progress
- Display a summary of successful downloads

---

## Requirements

- Python 3.x
- Install required packages using: `pip install -r requirements.txt`
  - requests
  - feedparser

---

## Error Handling

- **Retry Logic:** Failed downloads are automatically retried up to 3 times (configurable)
- **Exponential Backoff:** Retry delays increase exponentially (2, 4, 8 seconds)
- **RSS Feed Validation:** Invalid or unreachable feeds are logged and skipped
- **File System Safety:** Titles are sanitized to remove invalid filename characters
---
