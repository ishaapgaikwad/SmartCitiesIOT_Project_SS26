import json
import os
import sys

from flask import Flask, jsonify, render_template


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

import config


app = Flask(__name__)

NOTIFICATION_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "notifications.json"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/state")
def get_state():

    try:
        with open(config.STATE_FILE) as f:
            state = json.load(f)

        return jsonify(state)

    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({})


@app.route("/api/notifications")
def get_notifications():

    try:
        with open(NOTIFICATION_FILE) as f:
            notifications = json.load(f)

        return jsonify(notifications)

    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify([])


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )