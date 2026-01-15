import os
import hashlib
import numpy as np
from PIL import Image
from scipy.stats import chisquare

files = {
    "Suspect": "Picture_UAS_Steganografi.jpg",
    "Clean_WA": "Picture_UAS_Steganografi_fixnodata.jpg",
    "Super_Clean": "super_clean_baseline.jpg",
    "Steghide": "Picture_UAS_Steganografi_steghide.jpg",
    "OpenStego": "Picture_UAS_Steganografi_hidden.jpg"
}

data = {}
for k, v in files.items():
    if os.path.exists(v):
        raw = open(v, "rb").read()
        img = Image.open(v).convert("RGB")
        arr = np.array(img)
        lsbs = arr & 1
        flat_lsbs = lsbs.flatten()

        num_blocks = len(flat_lsbs) // 1024
        p_vals = []
        for i in range(num_blocks):
            block = flat_lsbs[i*1024:(i+1)*1024]
            obs = [np.sum(block == 0), np.sum(block == 1)]
            _, p = chisquare(obs, f_exp=[512, 512])
            p_vals.append(p)

        data[k] = {
            "size": os.path.getsize(v),
            "md5": hashlib.md5(raw).hexdigest(),
            "eoi": len([i for i in range(len(raw)) if raw[i:i+2] == b"\xff\xd9"]),
            "lsb": [np.mean(lsbs[:,:,i]) for i in range(3)],
            "chi": np.mean(p_vals)
        }

print("### TABLE 1: INTEGRITY")
print("| Label | Size | MD5 |")
print("| :--- | :--- | :--- |")
for k, v in data.items():
    print(f"| {k} | {v['size']:,} | `{v['md5']}` |")

print("\n### TABLE 2: EOI")
print("| Label | EOI Count |")
print("| :--- | :---: |")
for k, v in data.items():
    print(f"| {k} | {v['eoi']} |")

print("\n### TABLE 3: LSB STATS")
print("| Label | Red | Green | Blue |")
print("| :--- | :--- | :--- | :--- |")
for k, v in data.items():
    print(f"| {k} | {v['lsb'][0]:.6f} | {v['lsb'][1]:.6f} | {v['lsb'][2]:.6f} |")

print("\n### TABLE 4: CHI-SQUARE")
print("| Label | P-Value |")
print("| :--- | :--- |")
for k, v in data.items():
    print(f"| {k} | {v['chi']:.6f} |")
