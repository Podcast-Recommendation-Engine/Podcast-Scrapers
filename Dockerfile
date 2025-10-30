FROM python:3.13-alpine

RUN apk add --no-cache ffmpeg

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY src/ ./src/

CMD ["python", "src/main.py"]
