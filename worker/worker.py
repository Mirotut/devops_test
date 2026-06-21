from flask import Flask, jsonify
import time

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/task", methods=["POST"])
def receive_task():
    print("Worker received task", flush=True)
    print("Processing task...", flush=True)
    time.sleep(1)
    print("Task completed", flush=True)
    return jsonify({"status": "completed"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
