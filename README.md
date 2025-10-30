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
- Automatic conversion to WAV format using FFmpeg
- Sanitizes episode titles to create filesystem-friendly filenames
- Automatic retry logic with exponential backoff for failed downloads
- Date-prefixed filenames (YYYY-MM-DD format)
- Modular architecture with separated concerns (config, parsing, downloading, utilities)
- Configurable download parameters (retries, sleep time, save directory, max episodes)
- Docker support with docker-compose for easy deployment
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
│   ├── file_utils.py       # File name sanitization
│   └── audio_converter.py  # FFmpeg WAV conversion
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

# Convert downloaded audio to WAV format
CONVERT_TO_WAV = True
```

---

## Usage

### Option 1: Using Docker (Recommended)

1. **Configure RSS feeds:**
   - Edit `src/config/settings.py`
   - Add your RSS feed URLs to the `RSS_FEEDS` list

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build -d
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the scraper:**
   ```bash
   docker-compose down
   ```

### Option 2: Running Locally

1. **Install dependencies:**
   ```bash
   pip install -e .
   ```

2. **Install FFmpeg:**
   - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - **macOS:** `brew install ffmpeg`
   - **Linux:** `apt-get install ffmpeg`

3. **Configure RSS feeds:**
   - Edit `src/config/settings.py`
   - Add your RSS feed URLs to the `RSS_FEEDS` list

4. **Run the scraper:**
   ```bash
   cd src
   python main.py
   ```

The scraper will:
- Create the download directory if it doesn't exist
- Process each RSS feed sequentially
- Download audio files with sanitized, date-prefixed filenames
- Convert audio files to WAV format (if enabled)
- Provide detailed logging of the download progress
- Display a summary of successful downloads

---

## Requirements

- Python 3.13+
- FFmpeg (for WAV conversion)
- Docker & Docker Compose (optional, for containerized deployment)
- Dependencies (installed via pyproject.toml):
  - requests
  - feedparser

## Docker Configuration

The project includes Docker support with the following setup:

- **Named Volume:** `podcast_downloads` - Stores downloaded files persistently
- **Network:** `podcast_network` - Isolated bridge network for the container
- **Environment Variables:**
  - `PYTHONUNBUFFERED=1` - Real-time log output
  - `DOWNLOAD_DIR=/app/downloads` - Download directory path

### Accessing Downloaded Files

Files are stored in a Docker volume. To copy them to your local machine:

```bash
docker cp podcast-scraper:/app/downloads/. ./downloads/
```

Alternatively, modify `docker-compose.yml` to use a bind mount:

```yaml
volumes:
  - ./downloads:/app/downloads  # Direct folder mapping
```

---

## Audio Conversion

The scraper can automatically convert downloaded audio files to WAV format:

- **Format:** PCM signed 16-bit little-endian
- **Sample Rate:** 44100 Hz (CD quality)
- **Behavior:** Original MP3 files are deleted after successful conversion
- **Control:** Set `CONVERT_TO_WAV = False` in `settings.py` to disable

## Error Handling

- **Retry Logic:** Failed downloads are automatically retried up to 3 times (configurable)
- **Exponential Backoff:** Retry delays increase exponentially (2, 4, 8 seconds)
- **RSS Feed Validation:** Invalid or unreachable feeds are logged and skipped
- **File System Safety:** Titles are sanitized to remove invalid filename characters
- **Conversion Failures:** If FFmpeg conversion fails, the original file is preserved

---

## Notes

- RSS feed URLs can include authentication tokens if required
- The scraper respects rate limiting with configurable sleep time between downloads
- All downloaded files are saved with sanitized filenames in the format: `YYYY-MM-DD_episode_title.wav`
- Please ensure proper use in accordance with the terms of service of the RSS feed provider
- This script is intended for personal use and should be used responsibly

---
