#!/usr/bin/env bash
set -e

# Run initialization (create MinIO bucket if needed, create DB tables)
python -u app/init_service.py

# Start uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
