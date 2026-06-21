from flask import Flask, jsonify
import requests

app = Flask(__name__)

WORKER_URL = "http://worker:5001/task"


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/task")
def send_task():
    response = requests.post(WORKER_URL, timeout=10)
    return jsonify({"status": "task sent", "worker_response": response.json()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
