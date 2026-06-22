import os
import signal
import sys
import requests
from flask import Flask, jsonify

app = Flask(__name__)

WORKER_URL = os.environ.get("WORKER_URL", "http://worker:5001/task")


def _handle_sigterm(*_):
    sys.exit(0)


signal.signal(signal.SIGTERM, _handle_sigterm)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/task", methods=["GET", "POST"])
def send_task():
    resp = requests.post(WORKER_URL)
    return jsonify({"status": "task sent", "worker_response": resp.json()})


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    print("Application started", flush=True)
    app.run(host=host, port=port)
