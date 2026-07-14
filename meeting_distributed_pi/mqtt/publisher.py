import json

import paho.mqtt.client as mqtt

from config import (
    MQTT_BROKER,
    MQTT_STATE_TOPIC,
    MQTT_NOTIFICATION_TOPIC,
)


client = mqtt.Client()

client.connect(
    MQTT_BROKER,
    1883,
    60
)

client.loop_start()


def publish_state(state):

    payload = json.dumps(state)

    client.publish(
        MQTT_STATE_TOPIC,
        payload
    )


def publish_notification(notification):

    payload = json.dumps(notification)

    print()
    print("Publishing notification:")
    print(payload)

    result = client.publish(
        MQTT_NOTIFICATION_TOPIC,
        payload
    )

    print(
        "Notification MQTT result:",
        result.rc
    )
