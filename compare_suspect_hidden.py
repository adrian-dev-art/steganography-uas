import os
import numpy as np
from PIL import Image

file_suspect = "Picture_UAS_Steganografi.jpg"
file_hidden = "Picture_UAS_Steganografi_hidden.jpg"

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

print(f"--- SUSPECT VS HIDDEN COMPARISON ---")
print(f"File: {file_suspect}")
print(f"  Size: {os.path.getsize(file_suspect)} bytes")
print(f"  EOI Markers: {get_eoi_markers(file_suspect)}")
print(f"  LSB Stats: {get_lsb_stats(file_suspect)}")

print(f"\nFile: {file_hidden}")
print(f"  Size: {os.path.getsize(file_hidden)} bytes")
print(f"  EOI Markers: {get_eoi_markers(file_hidden)}")
print(f"  LSB Stats: {get_lsb_stats(file_hidden)}")
