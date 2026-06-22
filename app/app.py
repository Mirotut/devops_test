import json
import os
import signal
import sys

import redis
from flask import Flask, jsonify

app = Flask(__name__)

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def _handle_sigterm(*_):
    sys.exit(0)


signal.signal(signal.SIGTERM, _handle_sigterm)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/task", methods=["GET", "POST"])
def send_task():
    # Task delivery now goes through Redis — HTTP path to worker is removed.
    r.lpush("tasks", json.dumps({"task": "process"}))
    return jsonify({"status": "task queued"})


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    print("Application started", flush=True)
    app.run(host=host, port=port)
