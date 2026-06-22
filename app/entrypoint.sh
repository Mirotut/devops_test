#!/usr/bin/env bash
set -euo pipefail

echo "Starting App Container..."
bash startup.sh
exec python app.py
