import serial
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt 

# === USER SETTINGS ===
PORT = "/dev/ttyACM0"        # Change this to your Arduino port, e.g. "/dev/ttyUSB0" on Linux
BAUD = 9600
DURATION = 600        # seconds (10 minutes)

# === SETUP SERIAL ===
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  # Wait for Arduino reset

print(f"Logging data for {DURATION/60:.1f} minutes...")
last_val=0
def low_pass(val,alpha=0.1):
    return val*alpha + last_val*(1-alpha)

start_time = time.time()
data=[]
while (time.time() - start_time) < DURATION:
    line = ser.readline().decode("utf-8").strip()
    if line:
        try:
            value = int(line.split(",")[0])  # only first value if multiple
            timestamp = datetime.now().isoformat(timespec="milliseconds")
            last_val=low_pass(value)
            data.append(last_val)
            plt.cla()
            plt.plot(data)
            plt.pause(0.01)
            if len(data)>100:
                data.pop(0)
        except ValueError:
            # Ignore malformed lines
            pass

ser.close()
plt.show()
