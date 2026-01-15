import os
import numpy as np
from PIL import Image

files = {
    "Suspect": "Picture_UAS_Steganografi.jpg",
    "Hidden (OpenStego)": "Picture_UAS_Steganografi_hidden.jpg",
    "Clean (WhatsApp)": "Picture_UAS_Steganografi_fixnodata.jpg",
    "Baseline (Super Clean)": "super_clean.jpg"
}

def get_lsb_stats(path):
    img = Image.open(path)
    data = np.array(img)
    lsb = data & 1
    return [np.mean(lsb[:,:,i]) for i in range(3)]

def get_eoi_markers(path):
    with open(path, "rb") as f:
        content = f.read()
        markers = []
        index = 0
        while True:
            index = content.find(b'\xff\xd9', index)
            if index == -1: break
            markers.append(index)
            index += 2
        return markers

print(f"{'File Type':<25} | {'Size':<10} | {'EOI Count':<10} | {'LSB Avg (R,G,B)'}")
print("-" * 75)

for label, path in files.items():
    if os.path.exists(path):
        size = os.path.getsize(path)
        eois = get_eoi_markers(path)
        lsb = get_lsb_stats(path)
        lsb_str = ", ".join([f"{x:.4f}" for x in lsb])
        print(f"{label:<25} | {size:<10} | {len(eois):<10} | [{lsb_str}]")
    else:
        print(f"{label:<25} | Not found")
