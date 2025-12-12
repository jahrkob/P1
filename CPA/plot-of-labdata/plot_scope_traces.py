#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# ================================
# CONFIG
# ================================
FOLDER = "data/data-from-martinus"  # e.g. "data/data-from-scope"
PATTERN = "data_*.csv"                     # matches data_0.csv, data_1.csv, ...
CHANNEL_INDEX = 2      # 1 = CH1, 2 = CH2 (as in Keysight CSV)
SKIP_HEADER_LINES = 2  # Keysight: 2 header rows
MAX_TRACES_OVERLAY = 20  # how many traces to overlay in one plot


# ================================
# Helper: load one Keysight CSV
# ================================
def load_scope_csv(path, channel_index=2):
    """
    Load a Keysight-style CSV:
        x-axis,1,2
        second,Volt,Volt
        t0,ch1,ch2
        ...
    Returns:
        time: 1D array
        samples: 1D array (selected channel)
    """
    data = np.genfromtxt(path, delimiter=",", skip_header=SKIP_HEADER_LINES)
    time = data[:, 0]
    samples = data[:, channel_index]
    return time, samples


# ================================
# Load all traces
# ================================
file_paths = sorted(glob.glob(os.path.join(FOLDER, PATTERN)))
if not file_paths:
    raise FileNotFoundError(f"No files matching {os.path.join(FOLDER, PATTERN)}")

times = []
traces = []

for path in file_paths:
    t, s = load_scope_csv(path, CHANNEL_INDEX)
    times.append(t)
    traces.append(s)
    print(f"[+] Loaded {os.path.basename(path)}: {len(s)} samples")

# Check that all traces have same length
lengths = {len(s) for s in traces}
if len(lengths) != 1:
    raise ValueError(f"Not all traces have same length: {lengths}")

time = times[0]
traces = np.stack(traces, axis=0)  # shape: (num_traces, num_samples)
num_traces, num_samples = traces.shape
print(f"[+] Final traces array shape: {traces.shape}")


# ================================
# Plot 1: Single example trace
# ================================
plt.figure(figsize=(10, 4))
plt.plot(time * 1e6, traces[0])  # time in microseconds
plt.xlabel("Time (µs)")
plt.ylabel("Voltage (V)")
plt.title("Example power trace (CH2)")
plt.tight_layout()
plt.savefig("figure_example_trace.png", dpi=300)
# plt.show()


# ================================
# Plot 2: Overlay of first N traces
# ================================
n_overlay = min(MAX_TRACES_OVERLAY, num_traces)

plt.figure(figsize=(10, 4))
for i in range(n_overlay):
    plt.plot(time * 1e6, traces[i], alpha=0.3)
plt.xlabel("Time (µs)")
plt.ylabel("Voltage (V)")
plt.title(f"Overlay of {n_overlay} power traces")
plt.tight_layout()
plt.savefig("figure_overlay_traces.png", dpi=300)
# plt.show()


# ================================
# Plot 3: Mean ± std-dev
# ================================
mean_trace = traces.mean(axis=0)
std_trace = traces.std(axis=0)

plt.figure(figsize=(10, 4))
plt.plot(time * 1e6, mean_trace, label="Mean trace")
plt.fill_between(
    time * 1e6,
    mean_trace - std_trace,
    mean_trace + std_trace,
    alpha=0.3,
    label="±1 std-dev"
)
plt.xlabel("Time (µs)")
plt.ylabel("Voltage (V)")
plt.title("Mean power trace ± standard deviation")
plt.legend()
plt.tight_layout()
plt.savefig("figure_mean_std_trace.png", dpi=300)
# plt.show()

print("\nSaved figures:")
print("  figure_example_trace.png")
print("  figure_overlay_traces.png")
print("  figure_mean_std_trace.png")
