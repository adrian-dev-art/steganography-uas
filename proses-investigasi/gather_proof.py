import os
import hashlib
import numpy as np
from PIL import Image

file_suspect = "Picture_UAS_Steganografi.jpg"
file_clean = "Picture_UAS_Steganografi_fixnodata.jpg"

def get_md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def get_lsb_stats(path):
    img = Image.open(path)
    data = np.array(img)
    lsb = data & 1
    stats = []
    for i in range(3):
        stats.append(np.mean(lsb[:,:,i]))
    return stats

print(f"--- HASH ANALYSIS ---")
print(f"Suspect MD5: {get_md5(file_suspect)}")
print(f"Clean MD5:   {get_md5(file_clean)}")

print(f"\n--- SIZE ANALYSIS ---")
print(f"Suspect Size: {os.path.getsize(file_suspect)} bytes")
print(f"Clean Size:   {os.path.getsize(file_clean)} bytes")
print(f"Difference:   {os.path.getsize(file_suspect) - os.path.getsize(file_clean)} bytes")

print(f"\n--- LSB STATISTICAL ANALYSIS ---")
suspect_lsb = get_lsb_stats(file_suspect)
clean_lsb = get_lsb_stats(file_clean)
print(f"Suspect LSB (R,G,B): {suspect_lsb}")
print(f"Clean LSB (R,G,B):   {clean_lsb}")
print(f"LSB Difference:      {[s - c for s, c in zip(suspect_lsb, clean_lsb)]}")

print(f"\n--- HEX DIFFERENCE (FIRST 64 BYTES) ---")
with open(file_suspect, "rb") as f1, open(file_clean, "rb") as f2:
    b1 = f1.read(64)
    b2 = f2.read(64)
    for i in range(min(len(b1), len(b2))):
        if b1[i] != b2[i]:
            print(f"Offset {i:02x}: Suspect={b1[i]:02x} Clean={b2[i]:02x}")
