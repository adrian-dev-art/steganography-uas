import numpy as np
from PIL import Image
import os

def spa_channel(data):
    # Sample Pair Analysis (SPA) implementation
    # Estimates the embedding rate p
    x = 0
    y = 0
    k = 0
    for i in range(len(data) - 1):
        u = int(data[i])
        v = int(data[i+1])
        if (v % 2 == 0 and u < v) or (v % 2 == 1 and u > v):
            if (u + v) % 2 == 0: x += 1
            else: y += 1
        k += 1
    if x + y == 0: return 0
    return max(0, (x - y) / (x + y))

def analyze_file(path):
    img = Image.open(path).convert('RGB')
    arr = np.array(img)
    results = {}
    for i, channel in enumerate(['Red', 'Green', 'Blue']):
        data = arr[:,:,i].flatten()
        results[channel] = spa_channel(data)
    return results

files = {
    "Suspect": "Picture_UAS_Steganografi.jpg",
    "Clean": "super_clean_baseline.jpg",
    "Steghide": "Picture_UAS_Steganografi_steghide.jpg",
    "OpenStego": "Picture_UAS_Steganografi_hidden.jpg"
}

print(f"{'File':<15} | {'Red SPA':<10} | {'Green SPA':<10} | {'Blue SPA':<10}")
print("-" * 55)
for label, path in files.items():
    if os.path.exists(path):
        res = analyze_file(path)
        print(f"{label:<15} | {res['Red']:.6f} | {res['Green']:.6f} | {res['Blue']:.6f}")
