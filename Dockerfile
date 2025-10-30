FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY src/ ./src/

CMD ["python", "src/main.py"]
