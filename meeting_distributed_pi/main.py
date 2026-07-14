import time

import grovepi_driver as grovepi

from sensors.pir import setup as pir_setup
from sensors.fan import setup as fan_setup
from sensors.led import setup as led_setup
#from sensors.buzzer import setup as buzzer_setup
#from sensors.sound import setup as sound_setup

from context.state import update_context

from mqtt.publisher import publish_state
from mqtt.subscriber import client


grovepi.init()

pir_setup()
led_setup()
fan_setup()
#buzzer_setup()
#sound_setup()

client.loop_start()

previous_state = None

print("=== Raspberry Pi Sensor Node ===")

while True:

    try:

        state = update_context()

        if state != previous_state:

            print()
            print("Publishing state:")
            print(state)

            publish_state(state)

            previous_state = state.copy()

        time.sleep(1)

    except OSError as e:

        print("I2C Error:", e)

        time.sleep(1)

    except KeyboardInterrupt:

        break

client.loop_stop()
client.disconnect()
