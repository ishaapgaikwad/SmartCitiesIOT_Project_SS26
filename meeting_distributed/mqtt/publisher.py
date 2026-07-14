import paho.mqtt.client as mqtt

from config import MQTT_BROKER, MQTT_ACTION_TOPIC

client = mqtt.Client()

client.connect(MQTT_BROKER,1883,60)

client.loop_start()


def publish_action(action):

    client.publish(MQTT_ACTION_TOPIC,action)