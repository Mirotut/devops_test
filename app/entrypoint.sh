#!/bin/bash
set -euo pipefail

echo "Starting App Container..."
bash /app/init.sh
echo "Application started"

exec python app.py
