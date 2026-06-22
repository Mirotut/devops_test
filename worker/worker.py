import json
import logging
import os
import signal
import sys
import threading

import redis
from flask import Flask, jsonify

LOG_DIR = "/var/log/worker"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/worker.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

flask_app = Flask(__name__)


def _handle_sigterm(*_):
    sys.exit(0)


signal.signal(signal.SIGTERM, _handle_sigterm)


@flask_app.route("/health")
def health():
    return jsonify({"status": "ok"})


def run_health_server():
    flask_app.run(host="0.0.0.0", port=5001)


def consume():
    r = redis.Redis(
        host=os.environ.get("REDIS_HOST", "redis"),
        port=int(os.environ.get("REDIS_PORT", "6379")),
        decode_responses=True,
    )
    logger.info("Worker started, waiting for tasks...")
    while True:
        _, message = r.blpop("tasks")
        logger.info("Worker received task")
        logger.info("Processing task...")
        logger.info("Task completed")


if __name__ == "__main__":
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()
    consume()
