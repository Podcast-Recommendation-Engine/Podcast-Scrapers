# Podcast Scrapers

A Python-based podcast scraper that downloads episodes from RSS feeds, converts audio files to WAV format, and stores metadata in JSON.

## Features

- Fetch podcast episodes from multiple RSS feeds
- Download podcast audio files (MP3)
- Convert MP3 to WAV format with standardized audio settings (mono, 16kHz, 16-bit)
- Extract and store podcast metadata (title, duration, publish date, etc.)
- Docker support for containerized deployment
- Automatic cleanup of MP3 files after conversion

## Project Structure

```
Podcast-Scrapers/
├── src/
│   ├── config.py       # Configuration settings and constants
│   ├── main.py         # Main pipeline execution
│   └── utils.py        # Utility functions for scraping and processing
├── data/
│   ├── audio/          # Downloaded and converted audio files
│   └── raw/
│       └── podcasts.json  # Podcast metadata storage
├── docker/
│   ├── Dockerfile      # Docker image definition
│   ├── docker-compose.yml  # Docker Compose configuration
│   └── .dockerignore   # Docker ignore patterns
├── docs/               # Documentation files
├── pyproject.toml      # Python project dependencies
└── README.md           # This file
```

## Requirements

- Python 3.13+
- ffmpeg (for audio conversion)
- Dependencies listed in `pyproject.toml`:
  - feedparser
  - requests
  - pydub
  - audioop-lts

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/Podcast-Recommendation-Engine/Podcast-Scrapers.git
cd Podcast-Scrapers
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac
```

3. Install dependencies:
```bash
pip install -e .
```

4. Install ffmpeg:
   - Windows: Download from https://ffmpeg.org/download.html
   - Linux: `sudo apt-get install ffmpeg`
   - Mac: `brew install ffmpeg`

### Docker Setup

1. Build and run with Docker Compose:
```bash
cd docker
docker-compose up --build -d
```

2. View logs:
```bash
docker logs -f podcast-scraper
```

3. Stop the container:
```bash
docker-compose down
```

## Configuration

Edit `src/config.py` to configure:

- `RSS_FEEDS`: List of podcast RSS feed URLs
- `NUMBER_OF_PODCAST_FOR_EACH_PODCAST`: Number of episodes to download per feed
- `CHUNK_SIZE`: Download chunk size in bytes
- `AUDIO_PATH`: Directory for audio files
- `RAW_PATH`: Directory for JSON metadata
- `JSON_FILENAME`: Output JSON filename

## Usage

### Run Locally

```bash
python src/main.py
```

### Run with Docker

```bash
cd docker
docker-compose up -d
```

The scraper will:
1. Fetch episodes from configured RSS feeds
2. Download MP3 files to `data/audio/`
3. Convert MP3 to WAV format
4. Save metadata to `data/raw/podcasts.json`
5. Remove original MP3 files after conversion

## Audio Specifications

Converted WAV files have the following specifications:
- Channels: 1 (Mono)
- Sample Rate: 16kHz
- Sample Width: 16-bit

## Output Format

The JSON output contains episode metadata:
```json
{
  "id": "uuid4-string",
  "title": "Episode Title",
  "audio_url": "https://...",
  "year": 2025,
  "month": 11,
  "day": 17,
  "hour": 12,
  "minute": 0,
  "second": 0,
  "weekday": 0,
  "yearday": 321,
  "is_dst": 0,
  "subtitle": "Episode subtitle",
  "authors": [...],
  "image": "https://...",
  "itunes_duration": 165.37,
  "wav_path": "data/audio/episode.wav"
}
```

## Development

### Adding New RSS Feeds

Add feed URLs to the `RSS_FEEDS` list in `src/config.py`:
```python
RSS_FEEDS = [
    "https://example.com/feed/podcast/",
    "https://another-podcast.com/rss"
]
```

### Error Handling

The application includes error handling for:
- Network failures during feed fetching
- Invalid RSS feed formats
- Download interruptions
- Audio conversion errors
- Invalid duration formats

## License

This project is part of the Podcast Recommendation Engine system.