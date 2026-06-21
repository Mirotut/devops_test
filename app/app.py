from flask import Flask, jsonify
import redis
import json

app = Flask(__name__)
r = redis.Redis(host="redis", port=6379, decode_responses=True)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/task")
def send_task():
    task = {"task": "process", "data": "sample"}
    r.rpush("tasks", json.dumps(task))
    return jsonify({"status": "task queued via redis"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
