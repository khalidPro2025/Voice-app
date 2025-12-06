#!/usr/bin/env bash
set -e

cd /app

# Initialisation (bucket + tables)
python -u app/init_service.py

# Lancer FastAPI
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

