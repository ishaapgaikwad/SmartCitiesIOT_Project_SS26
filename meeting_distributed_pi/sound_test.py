import time
import grovepi_driver as grovepi

grovepi.init()

print("=== Sound Sensor Test ===")

try:

    while True:

        value = grovepi.analogRead(0)

        print("Sound Level:", value)

        time.sleep(0.5)

except KeyboardInterrupt:

    print("Stopped.")
