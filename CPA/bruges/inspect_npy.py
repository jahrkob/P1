import numpy as np

TRACES_PATH = "data/premade/traces.npy"
TEXTINS_PATH = "data/premade/textins.npy"

traces = np.load(TRACES_PATH)
textins = np.load(TEXTINS_PATH)

print("traces.shape:", traces.shape, "dtype:", traces.dtype)
print("textins.shape:", textins.shape, "dtype:", textins.dtype)

# Vis første trace (kun de første 20 samples)
print("\nFirst trace, first 20 samples:")
print(traces[0, :20])

# Vis første 5 plaintexts (16 bytes hver)
print("\nFirst 5 plaintexts (hex):")
for i in range(min(5, textins.shape[0])):
    print(i, " ".join(f"{b:02x}" for b in textins[i]))

# Min/max for at sanity-checke
print("\ntraces min/max:", float(traces.min()), float(traces.max()))
