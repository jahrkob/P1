#!/usr/bin/env python3
import numpy as np
import csv

# =========================================
# CONFIGURATION
# =========================================
TRACES_PATH   = "data/data-from-daniel/4/aes_traces_20251202_095012_traces300.csv"
METADATA_PATH = "data/data-from-daniel/4/aes_traces_20251202_095012_metadata300.csv"

# Limit which bytes to attack (0..15). For all 16, use range(16).
BYTES_TO_ATTACK = range(16)


# =========================================
# Helpers for parsing
# =========================================
def parse_hex_bytes(s: str) -> np.ndarray:
    """
    Parse a hex string into a 1D uint8 array of bytes.
    Accepts:
      "00112233..." or "0x001122..." or "00 11 22 33 ..."
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
    Load traces from CSV with header: trace_id, s0, s1, ..., sN
    Returns: (num_traces, num_samples) float32
    """
    with open(path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        n_cols = len(header)

    data = np.genfromtxt(
        path,
        delimiter=",",
        skip_header=1,
        usecols=range(1, n_cols),  # skip trace_id
        dtype=float,
    )
    if data.ndim == 1:
        data = data.reshape(1, -1)
    return data.astype(np.float32)


def load_plaintexts_and_key_from_metadata(path: str):
    """
    Load plaintexts and key from metadata CSV with header:
        trace_id,plaintext,ciphertext,key

    Returns:
        plaintexts: (N, 16) uint8
        true_key:   (16,)  uint8
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
            key_bytes = parse_hex_bytes(key_str)

            plaintexts.append(pt_bytes)
            keys.append(key_bytes)

    plaintexts = np.stack(plaintexts, axis=0)  # (N, 16) if AES-128
    keys = np.stack(keys, axis=0)              # (N, 16)

    first_key = keys[0]
    if not np.all((keys == first_key).all(axis=1)):
        print("[!] Warning: not all key rows in metadata are identical.")

    if plaintexts.shape[1] != 16:
        print(f"[!] Warning: plaintexts have {plaintexts.shape[1]} bytes per row (expected 16).")

    return plaintexts.astype(np.uint8), first_key


# =========================================
# Load data
# =========================================
traces = load_traces_from_csv(TRACES_PATH)
textins, true_key = load_plaintexts_and_key_from_metadata(METADATA_PATH)

num_traces, trace_length = traces.shape
num_plain_bytes = textins.shape[1]

print(f"[+] Loaded traces:   {TRACES_PATH}   -> {traces.shape}")
print(f"[+] Loaded metadata: {METADATA_PATH} -> {textins.shape}")
print(f"[+] Number of plaintext bytes: {num_plain_bytes}")

# Sanity check
for b in BYTES_TO_ATTACK:
    if b < 0 or b >= num_plain_bytes:
        raise ValueError(
            f"Byte index {b} in BYTES_TO_ATTACK is out of range for {num_plain_bytes} plaintext bytes."
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


def key_to_hex(k):
    return " ".join(f"{b:02x}" for b in k)


def key_to_ascii(k):
    return "".join(chr(b) if 32 <= b <= 126 else "." for b in k)


# =========================================
# Multi-byte CPA: scan POIs per byte
# =========================================
recovered_key = np.zeros(16, dtype=np.uint8)
best_pois = np.full(16, -1, dtype=int)
best_corrs = np.zeros(16, dtype=float)

for byte_idx in BYTES_TO_ATTACK:
    print(f"\n[+] Scanning POIs for plaintext byte index {byte_idx} over all {trace_length} samples")

    pbytes = textins[:, byte_idx]

    # Precompute hypothetical leakage for all 256 guesses: (N, 256)
    key_guesses = np.arange(256, dtype=np.uint8)
    inter_all = SBOX[pbytes[:, None] ^ key_guesses[None, :]]  # (N, 256)
    hyp_all = HW[inter_all].astype(np.float64)                 # (N, 256)

    hyp_mean = hyp_all.mean(axis=0)                 # (256,)
    hyp_centered = hyp_all - hyp_mean               # (N, 256)
    hyp_var = np.sum(hyp_centered ** 2, axis=0)     # (256,)

    best_overall_corr = -1.0
    best_overall_guess = None
    best_overall_poi = None

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

        if best_corr > best_overall_corr:
            best_overall_corr = best_corr
            best_overall_guess = best_idx
            best_overall_poi = poi

    recovered_key[byte_idx] = best_overall_guess
    best_pois[byte_idx] = best_overall_poi
    best_corrs[byte_idx] = best_overall_corr

    print(f"    -> best POI for byte {byte_idx}: {best_overall_poi}")
    print(f"       best key guess: 0x{best_overall_guess:02x}  (|corr| = {best_overall_corr:.5f})")

# =========================================
# Summary
# =========================================
print("\n==============================")
print("Recovered key (hex):")
print(key_to_hex(recovered_key))
print("Recovered key (ASCII-ish):")
print(key_to_ascii(recovered_key))

print("\nTrue key (from metadata) (hex):")
print(key_to_hex(true_key))

matches = np.sum(recovered_key == true_key)
print(f"\nByte-wise matches: {matches}/16")

print("\nBest POI per key byte:")
for i in range(16):
    print(f"  byte {i:2d}: POI={best_pois[i]:4d},  corr={best_corrs[i]:.5f}")
