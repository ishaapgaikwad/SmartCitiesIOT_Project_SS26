import json
import os

import paho.mqtt.client as mqtt

import config

from planner.problem_generator import generate_problem
from planner.run_planner import run_planner
from mqtt.publisher import publish_action


MAX_NOTIFICATIONS = 100

NOTIFICATION_FILE = os.path.join(
    "data",
    "notifications.json"
)


def save_notification(notification):

    try:
        with open(NOTIFICATION_FILE, "r") as f:
            notifications = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        notifications = []

    notifications.append(notification)

    notifications = notifications[-MAX_NOTIFICATIONS:]

    with open(NOTIFICATION_FILE, "w") as f:
        json.dump(
            notifications,
            f,
            indent=4
        )

    print("Notification saved to:", NOTIFICATION_FILE)


def on_message(client, userdata, msg):

    # ==========================================
    # SENSOR STATE MESSAGE
    # ==========================================

    if msg.topic == config.MQTT_STATE_TOPIC:

        state = json.loads(
            msg.payload.decode()
        )

        with open(config.STATE_FILE, "w") as f:
            json.dump(
                state,
                f,
                indent=4
            )

        print()
        print("Received state:", state)

        generate_problem()

        actions = run_planner()

        print("Planner actions:", actions)

        for action in actions:
            publish_action(action)


    # ==========================================
    # NOTIFICATION MESSAGE
    # ==========================================

    elif msg.topic == config.MQTT_NOTIFICATION_TOPIC:

        notification = json.loads(
            msg.payload.decode()
        )

        print()
        print("Received notification:", notification)

        save_notification(notification)


client = mqtt.Client()

client.on_message = on_message

client.connect(
    config.MQTT_BROKER,
    1883,
    60
)

client.subscribe(
    config.MQTT_STATE_TOPIC
)

client.subscribe(
    config.MQTT_NOTIFICATION_TOPIC
)

print("Subscribed to:")
print(" -", config.MQTT_STATE_TOPIC)
print(" -", config.MQTT_NOTIFICATION_TOPIC)