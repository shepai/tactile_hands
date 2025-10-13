import serial
import time
import csv
from datetime import datetime

# === USER SETTINGS ===
PORT = "/dev/ttyACM1"        # Change this to your Arduino port, e.g. "/dev/ttyUSB0" on Linux
BAUD = 9600
DURATION = 600        # seconds (10 minutes)
OUTPUT_FILE = "/its/home/drs25/Documents/GitHub/tactile_hands/Experimental/data/cap0.1uf/ads7830_rubber_100g.csv"

# === SETUP SERIAL ===
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  # Wait for Arduino reset

print(f"Logging data for {DURATION/60:.1f} minutes...")

# === OPEN CSV FILE ===
with open(OUTPUT_FILE, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "value"])  # header row

    start_time = time.time()

    while (time.time() - start_time) < DURATION:
        line = ser.readline().decode("utf-8").strip()
        if line:
            try:
                value = int(line.split(",")[0])  # only first value if multiple
                timestamp = datetime.now().isoformat(timespec="milliseconds")
                writer.writerow([timestamp, value])
                print(f"{timestamp} -> {value}")
            except ValueError:
                # Ignore malformed lines
                pass

ser.close()
print(f"\n✅ Saved data to {OUTPUT_FILE}")
