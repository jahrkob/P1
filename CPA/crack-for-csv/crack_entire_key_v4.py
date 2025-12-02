#!/usr/bin/env python3
import numpy as np
import os
import csv

# =========================================
# CONFIGURATION
# =========================================
# DATASET_TYPE options:
#   "single_scan" -> only one plaintext byte leaks, POI unknown → scan all samples
#   "single"      -> only one plaintext byte leaks at known POI (after you've scanned)
#
# (You *can* extend this later to multi-byte / full-key if your leakage supports it.)
DATASET_TYPE = "single_scan"    # "single_scan" or "single"

# Paths to your files (CSV with header: trace_id,plaintext,ciphertext,key)
TRACES_PATH   = "data/data-from-daniel/aes_traces_20251201_143819_traces300.csv"
TEXTINS_PATH  = "data/data-from-daniel/aes_traces_20251201_143819_metadata300.csv"

# If you have a separate key file (e.g. synthetic dataset), you can set it here.
# But since your metadata already contains the key, we parse it from there.
TRUE_KEY_PATH = None  # keep None; we'll use metadata "key" column

# Which plaintext byte to attack (0–15 for a 16-byte plaintext)
SINGLE_BYTE_INDEX = 0

# Only used in DATASET_TYPE="single", after you've found the POI with single_scan
SINGLE_BYTE_POI   = 50


# =========================================
# Helpers for parsing
# =========================================
def parse_hex_bytes(s: str) -> np.ndarray:
    """
    Parse a hex string into a 1D uint8 array of bytes.
    Accepts formats like:
        "00112233445566778899aabbccddeeff"
        "0x00112233445566778899aabbccddeeff"
        "00 11 22 33 ..." (spaces ignored)
    """
    s = s.strip()
    if s.startswith("0x") or s.startswith("0X"):
        s = s[2:]
    s = s.replace(" ", "")
    if len(s) % 2 != 0:
        raise ValueError(f"Hex string has odd length: {s!r}")
    return np.array([int(s[i:i+2], 16) for i in range(0, len(s), 2)], dtype=np.uint8)


def load_traces_from_csv(path: str) -> np.ndarray:
    """
    Load traces from CSV with a header whose first column is 'trace_id'
    and the remaining columns are numeric samples.
    """
    # Read header to know how many columns
    with open(path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        n_cols = len(header)

    # usecols=range(1, n_cols) -> skip first col (trace_id)
    data = np.genfromtxt(
        path,
        delimiter=",",
        skip_header=1,
        usecols=range(1, n_cols),
        dtype=float
    )
    if data.ndim == 1:
        data = data.reshape(1, -1)
    return data.astype(np.float32)


def load_plaintexts_and_key_from_metadata(path: str):
    """
    Load plaintexts and key from metadata CSV with header:
        trace_id,plaintext,ciphertext,key

    Returns:
        plaintexts: (N, 16) uint8 (assuming 16-byte AES)
        true_key:   (16,) uint8 or None if key cannot be parsed
    """
    plaintexts = []
    keys = []

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        expected_fields = ["trace_id", "plaintext", "ciphertext", "key"]
        for field in expected_fields:
            if field not in reader.fieldnames:
                raise ValueError(
                    f"Expected column '{field}' in metadata CSV, found {reader.fieldnames}"
                )

        for row in reader:
            pt_str = row["plaintext"]
            key_str = row["key"]

            pt_bytes = parse_hex_bytes(pt_str)
            plaintexts.append(pt_bytes)

            # Key is the same for all traces, but we parse every row and check consistency later
            key_bytes = parse_hex_bytes(key_str)
            keys.append(key_bytes)

    plaintexts = np.stack(plaintexts, axis=0)  # (N, 16) if AES-128
    keys = np.stack(keys, axis=0)              # (N, 16)

    # Check that all keys are identical across rows
    first_key = keys[0]
    if not np.all((keys == first_key).all(axis=1)):
        print("[!] Warning: not all key rows in metadata are identical.")

    true_key = first_key

    if plaintexts.shape[1] != 16:
        print(f"[!] Warning: plaintexts have {plaintexts.shape[1]} bytes per row (expected 16 for AES-128).")

    return plaintexts.astype(np.uint8), true_key


# =========================================
# Load data
# =========================================
traces = load_traces_from_csv(TRACES_PATH)
textins, true_key = load_plaintexts_and_key_from_metadata(TEXTINS_PATH)

num_traces, trace_length = traces.shape
num_plain_bytes = textins.shape[1]

print(f"[+] Loaded traces:   {TRACES_PATH}  -> {traces.shape}")
print(f"[+] Loaded metadata: {TEXTINS_PATH} -> {textins.shape}")
print(f"[+] Number of plaintext bytes: {num_plain_bytes}")
print(f"[+] Dataset type: {DATASET_TYPE}")

if SINGLE_BYTE_INDEX < 0 or SINGLE_BYTE_INDEX >= num_plain_bytes:
    raise ValueError(
        f"SINGLE_BYTE_INDEX={SINGLE_BYTE_INDEX} is out of range for {num_plain_bytes} plaintext bytes."
    )


# =========================================
# AES S-box and Hamming weight
# =========================================
SBOX = np.array([
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
], dtype=np.uint8)

HW = np.array([bin(x).count("1") for x in range(256)], dtype=np.float32)


# =========================================
# Pearson correlation
# =========================================
def pearson_corr(x, y):
    x = x.astype(np.float64)
    y = y.astype(np.float64)
    x = x - x.mean()
    y = y - y.mean()
    num = np.dot(x, y)
    den = np.sqrt(np.dot(x, x) * np.dot(y, y))
    if den == 0:
        return 0.0
    return num / den


# =========================================
# Small helpers
# =========================================
def key_to_hex(k):
    return " ".join(f"{b:02x}" for b in k)

def key_to_ascii(k):
    return "".join(chr(b) if 32 <= b <= 126 else "." for b in k)


# =========================================
# CPA attack
# =========================================
if DATASET_TYPE == "single_scan":
    # Only one plaintext byte leaks, POI unknown -> scan all samples
    recovered_key = np.zeros(num_plain_bytes, dtype=np.uint8)

    byte_idx = SINGLE_BYTE_INDEX
    pbytes = textins[:, byte_idx]

    print(f"\n[+] Scanning POIs for leaking plaintext byte index {byte_idx} over all {trace_length} samples")

    # Precompute hypothetical leakage matrix: shape (N, 256)
    key_guesses = np.arange(256, dtype=np.uint8)
    inter_all = SBOX[pbytes[:, None] ^ key_guesses[None, :]]  # (N, 256)
    hyp_all = HW[inter_all].astype(np.float64)                 # (N, 256)

    hyp_mean = hyp_all.mean(axis=0)                 # (256,)
    hyp_centered = hyp_all - hyp_mean               # (N, 256)
    hyp_var = np.sum(hyp_centered ** 2, axis=0)     # (256,)

    best_overall_corr = -1.0
    best_overall_guess = None
    best_overall_poi = None

    best_corr_per_poi = np.zeros(trace_length)
    best_guess_per_poi = np.zeros(trace_length, dtype=np.int32)

    for poi in range(trace_length):
        samples = traces[:, poi].astype(np.float64)
        samples_centered = samples - samples.mean()
        s_var = np.sum(samples_centered ** 2)

        if s_var == 0:
            continue

        num = np.dot(samples_centered, hyp_centered)  # (256,)
        den = np.sqrt(hyp_var * s_var)               # (256,)
        corr_all = np.abs(num / den)

        best_idx = int(np.argmax(corr_all))
        best_corr = float(corr_all[best_idx])

        best_corr_per_poi[poi] = best_corr
        best_guess_per_poi[poi] = best_idx

        if best_corr > best_overall_corr:
            best_overall_corr = best_corr
            best_overall_guess = best_idx
            best_overall_poi = poi

    print(f"\n[+] Best overall POI: {best_overall_poi}")
    print(f"    -> best key guess at that POI: 0x{best_overall_guess:02x} (|corr| = {best_overall_corr:.5f})")

    # Top 10 POIs
    top_k = min(10, trace_length)
    idx_sorted = np.argsort(-best_corr_per_poi)[:top_k]
    print(f"\n[+] Top {top_k} POIs by max correlation:")
    for rank, poi in enumerate(idx_sorted, start=1):
        print(f"   #{rank}: POI {poi:3d}  best_guess=0x{best_guess_per_poi[poi]:02x}  "
              f"|corr|={best_corr_per_poi[poi]:.5f}")

    recovered_key[byte_idx] = best_overall_guess

elif DATASET_TYPE == "single":
    # Only one plaintext byte leaks at a known POI
    recovered_key = np.zeros(num_plain_bytes, dtype=np.uint8)

    byte_idx = SINGLE_BYTE_INDEX
    poi = SINGLE_BYTE_POI

    if poi >= trace_length:
        raise ValueError(f"POI {poi} out of range for trace length {trace_length}")

    samples = traces[:, poi]
    pbytes = textins[:, byte_idx]

    best_corr = -1.0
    best_guess = 0

    print(f"\n[+] Attacking plaintext byte index {byte_idx} at POI {poi}")

    for kguess in range(256):
        inter = SBOX[pbytes ^ kguess]
        hyp = HW[inter]
        corr = abs(pearson_corr(hyp, samples))

        if corr > best_corr:
            best_corr = corr
            best_guess = kguess

    recovered_key[byte_idx] = best_guess
    print(f"    -> best guess for byte {byte_idx}: 0x{best_guess:02x}  (|corr| = {best_corr:.5f})")

else:
    raise ValueError(f"Unsupported DATASET_TYPE for this real-hardware format: {DATASET_TYPE!r}")


# =========================================
# Print results
# =========================================
print("\n==============================")
print("Recovered key bytes (hex):")
print(key_to_hex(recovered_key))
print("Recovered key (ASCII-ish):")
print(key_to_ascii(recovered_key))

if true_key is not None and true_key.size >= recovered_key.size:
    # Compare only the bytes we actually recovered
    tk_slice = true_key[:recovered_key.size]
    print("\nTrue key (from metadata 'key' column) (hex):")
    print(key_to_hex(tk_slice))

    matches = np.sum(recovered_key == tk_slice)
    print(f"\nByte-wise matches in first {recovered_key.size} bytes: {matches}/{recovered_key.size}")
    if matches == recovered_key.size:
        print("[+] All recovered bytes match these positions of the true key 🎉")
    else:
        print("[!] Not all recovered bytes match the corresponding true-key bytes.")
