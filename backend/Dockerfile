FROM python:3.11-slim

# Install system deps (ffmpeg, build tools, git)
RUN apt-get update && \
    apt-get install -y ffmpeg gcc libpq-dev git && \
    rm -rf /var/lib/apt/lists/*

# Dossier de travail
WORKDIR /app

# Copier requirements
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Copier l'application backend
COPY app /app/app

# Copier script d'entrée
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["/app/entrypoint.sh"]

