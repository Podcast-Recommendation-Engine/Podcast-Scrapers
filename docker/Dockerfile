FROM python:3.13-slim

WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY src/ ./src/

RUN pip install --no-cache-dir .

RUN mkdir -p /app/data/audio /app/data/raw

CMD ["python", "src/main.py"]