FROM python:3.11-slim

# Install system deps (ffmpeg, build tools for some wheels)
RUN apt-get update && \
    apt-get install -y ffmpeg gcc libpq-dev  git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

CMD ["/entrypoint.sh"]
