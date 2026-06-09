"""
generate_data.py
----------------
Generates fake sensor data (voltage, current, temperature) and saves it
to 'sensor_data.csv' for use with the plotter script.
"""

import csv
import random
import math
from datetime import datetime, timedelta
import logging

logger=logging.getLogger(__name__)

OUTPUT_FILE = "sensor_data.csv"
NUM_SAMPLES = 200
START_TIME = datetime(2024, 1, 1, 0, 0, 0)
INTERVAL_SECONDS = 30  # one reading every 30 seconds

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def generate_sensor_readings(num_samples: int):
    try:
        """
        Simulate realistic sensor readings with gradual trends and small noise.

        Returns a list of dicts with keys: timestamp, voltage, current, temperature
        """
        readings = []

        for i in range(num_samples):
            timestamp = START_TIME + timedelta(seconds=i * INTERVAL_SECONDS)

            # Voltage: stable around 12V with small fluctuations
            voltage = 12.0 + 0.5 * math.sin(i / 20) + random.gauss(0, 0.1)

            # Current: gradual increase (simulating load rising) + noise
            current = 2.0 + (i / num_samples) * 3.0 + random.gauss(0, 0.15)

            # Temperature: rises with current, then levels off (thermal curve)
            temperature = (
                25.0 + 0.08 * current * i / num_samples * 30 + random.gauss(0, 0.5)
            )

            readings.append(
                {
                    "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "voltage": round(voltage, 4),
                    "current": round(current, 4),
                    "temperature": round(temperature, 4),
                }
            )

        return readings

    except Exception as e:
        logger.error("Failed to generate sensor readings",e)


def save_to_csv(readings, filename: str):
    try:
        """Write readings list to a CSV file."""
        fieldnames = ["timestamp", "voltage", "current", "temperature"]

        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(readings)

        logger.info("Saved %d records to '%s'", len(readings), filename)

    except Exception:
        logger.error("Failed to save readings list to CSV file")
        raise


if __name__ == "__main__":
    logger.info("[*] Generating fake sensor data...")
    data = generate_sensor_readings(NUM_SAMPLES)
    save_to_csv(data, OUTPUT_FILE)
    logger.info("[✓] Done! Run 'python plot_sensor_data.py' to visualize.")
