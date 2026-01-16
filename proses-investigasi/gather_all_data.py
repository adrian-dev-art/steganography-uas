import hashlib
import os
import numpy as np
from PIL import Image

files = {
    "Suspect": "Picture_UAS_Steganografi.jpg",
    "Clean_WA": "Picture_UAS_Steganografi_fixnodata.jpg",
    "Super_Clean": "super_clean_baseline.jpg",
    "Steghide": "Picture_UAS_Steganografi_steghide.jpg",
    "OpenStego": "Picture_UAS_Steganografi_hidden.jpg"
}

def get_md5(path):
    if not os.path.exists(path): return "N/A"
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def get_lsb_stats(path):
    if not os.path.exists(path): return [0, 0, 0]
    img = Image.open(path)
    data = np.array(img)
    lsb = data & 1
    return [np.mean(lsb[:,:,i]) for i in range(3)]

def get_eoi(path):
    if not os.path.exists(path): return []
    content = open(path, "rb").read()
    return [i for i in range(len(content)) if content[i:i+2] == b'\xff\xd9']

print(f"{'Label':<15} | {'Size':<10} | {'MD5 Hash':<35} | {'LSB (R,G,B)':<30} | {'EOI Count'}")
print("-" * 110)
for label, path in files.items():
    if os.path.exists(path):
        size = os.path.getsize(path)
        md5 = get_md5(path)
        lsb = get_lsb_stats(path)
        lsb_str = ", ".join([f"{x:.6f}" for x in lsb])
        eoi = get_eoi(path)
        print(f"{label:<15} | {size:<10} | {md5:<35} | {lsb_str:<30} | {len(eoi)}")
