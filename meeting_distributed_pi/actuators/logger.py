import csv
import os
from datetime import datetime

import config


def log_event(action, state):

    os.makedirs(config.LOG_DIR, exist_ok=True)

    file_exists = os.path.exists(config.LOG_FILE)

    with open(config.LOG_FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not file_exists:

            writer.writerow([
                "Timestamp",
                "Planner Action",
                "Occupied",
                "Temperature",
                "Humidity",
                "Air Quality",
                "Air Quality Value",
                "Light",
                "Fan"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            action,
            state["occupied"],
            state["temperature"],
            state["humidity"],
            state["air_quality"],
            state["air_quality_value"],
            state["light"],
            state["fan"]
        ])

    print("Logger: Event saved.")
