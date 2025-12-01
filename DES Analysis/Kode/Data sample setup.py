
import pyvisa
import serial
import time

# 1. Forbind til oscilloskopet
rm = pyvisa.ResourceManager()
scope = rm.open_resource('USB0::0x2A8D::0x1797::MY12345678::INSTR')  # Tilpas ID

# 2. Forbind til Arduino
arduino = serial.Serial('COM3', 9600)  # Tilpas COM-port

# 3. Konfigurer oscilloskopet
scope.write(":STOP")
scope.write(":TRIGger:EDGE:SOURce CHANnel1")
scope.write(":TRIGger:EDGE:LEVel 0.5")
scope.write(":RUN")

# 4. Loop for at vente på trigger fra Arduino
while True:
    if arduino.readline().decode().strip() == "TRIGGER":
        print("Trigger modtaget fra Arduino!")
        
        # Vent til oscilloskopet har fanget signalet
        time.sleep(0.5)
        
        # Hent data
        scope.write(":WAVeform:SOURce CHANnel1")
        scope.write(":WAVeform:FORMat ASCii")
        data = scope.query(":WAVeform:DATA?")
        
        # Gem data
        with open("capture.csv", "a") as f:
            f.write(data + "\n")
        
        print("Data gemt!")
