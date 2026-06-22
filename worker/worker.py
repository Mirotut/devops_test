import os
import signal
import sys
from flask import Flask, jsonify

app = Flask(__name__)


def _handle_sigterm(*_):
    sys.exit(0)


signal.signal(signal.SIGTERM, _handle_sigterm)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/task", methods=["GET", "POST"])
def receive_task():
    print("Worker received task", flush=True)
    print("Processing task...", flush=True)
    print("Task completed", flush=True)
    return jsonify({"status": "completed"})


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5001"))
    app.run(host=host, port=port)
