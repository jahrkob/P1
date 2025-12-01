
import pyvisa
import serial
import time
import csv
from datetime import datetime
from tqdm import tqdm  # progress-bar

# === KONFIGURATION ===
OSC_VISA_ADDRESS = "USB0::0x2A8D::0x1797::MY12345678::INSTR"  # Tilpas til dit scope
ARDUINO_PORT = "COM3"  # Tilpas til din Arduino
BAUDRATE = 9600
OSC_CHANNEL = "MATH"  # Math.5 (Channel1 - Channel2)
NUM_MEASUREMENTS = 1000
CSV_FILE = "oscilloscope_data.csv"

# === Forbind til oscilloskop ===
rm = pyvisa.ResourceManager()
print("Søger efter oscilloskop...")
scope = rm.open_resource(OSC_VISA_ADDRESS)
scope.timeout = 5000  # 5 sekunder timeout

# === Forbind til Arduino ===
print("Forbinder til Arduino...")
arduino = serial.Serial(ARDUINO_PORT, BAUDRATE, timeout=1)

# === Konfigurer oscilloskop ===
print("Konfigurerer oscilloskop...")
scope.write(":STOP")
scope.write(f":WAVeform:SOURce {OSC_CHANNEL}")
scope.write(":WAVeform:FORMat ASCii")  # ASCII for nem CSV
scope.write(":TRIGger:SOURce EXT")  # Ekstern trigger
scope.write(":RUN")

# === Forbered CSV-fil ===
with open(CSV_FILE, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "VoltValues"])  # Header

print(f"Starter målinger ({NUM_MEASUREMENTS} målinger)...")

# === Loop med progress-bar ===
try:
    with tqdm(total=NUM_MEASUREMENTS, desc="Optager data", unit="måling") as pbar:
        count = 0
        while count < NUM_MEASUREMENTS:
            line = arduino.readline().decode(errors='ignore').strip()
            if line == "TRIGGER":
                ts = datetime.now().isoformat(timespec='seconds')

                # Vent lidt for at sikre data er klar
                time.sleep(0.5)

                # Hent waveform-data
                data = scope.query(":WAVeform:DATA?")
                volt_values = data.strip()

                # Gem i CSV
                with open(CSV_FILE, mode="a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([ts, volt_values])

                count += 1
                pbar.update(1)

    print(" Alle målinger er færdige! Data gemt i", CSV_FILE)

except KeyboardInterrupt:
    print("\n Målinger stoppet manuelt. Data gemt indtil nu i", CSV_FILE)

except Exception as e:
    print("\n Fejl opstod:", e)
