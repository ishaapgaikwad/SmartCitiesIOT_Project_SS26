import time
import grovepi_driver as grovepi

grovepi.init()

AIR_PORT = 1

print("=== Grove Air Quality Sensor Test ===")
print("Press Ctrl+C to stop.\n")

while True:
    try:
        value = grovepi.analogRead(AIR_PORT)
        print(f"Air Quality Value: {value}")
        time.sleep(1)

    except KeyboardInterrupt:
        print("\nTest stopped.")
        break

    except Exception as e:
        print("Error:", e)
        time.sleep(1)
