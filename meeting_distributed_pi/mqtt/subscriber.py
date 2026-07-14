import paho.mqtt.client as mqtt

from config import (
    MQTT_BROKER,
    MQTT_ACTION_TOPIC,
)

from actuators.execute_actions import execute_action


def on_message(client, userdata, msg):

    action = msg.payload.decode()

    print()
    print("Received planner action:", action)

    execute_action(action)


client = mqtt.Client()

client.on_message = on_message

client.connect(
    MQTT_BROKER,
    1883,
    60
)

client.subscribe(
    MQTT_ACTION_TOPIC
)
