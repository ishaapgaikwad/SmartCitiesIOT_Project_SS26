import time
import grovepi

PIR_PORT = 4   # Change this if your PIR is plugged into another port

grovepi.pinMode(PIR_PORT, "INPUT")

print("Testing PIR sensor... Press Ctrl+C to stop.")

while True:
    try:
        value = grovepi.digitalRead(PIR_PORT)
        print(value)
        time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopped.")
        break
