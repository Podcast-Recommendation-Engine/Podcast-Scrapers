FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ ./src/

# RUN pip install --no-cache-dir .
RUN pip install --no-cache-dir . && rm -rf build

# RUN mkdir -p /app/data/audio /app/data/raw

CMD ["python", "src/main.py"]