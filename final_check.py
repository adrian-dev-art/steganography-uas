import numpy as np
from PIL import Image
from scipy.stats import chisquare
import os
import hashlib

files = {
    "Suspect": "Picture_UAS_Steganografi.jpg",
    "Clean_WA": "Picture_UAS_Steganografi_fixnodata.jpg",
    "Super_Clean": "super_clean_baseline.jpg",
    "Steghide": "Picture_UAS_Steganografi_steghide.jpg",
    "OpenStego": "Picture_UAS_Steganografi_hidden.jpg"
}

def get_md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def get_eoi(path):
    content = open(path, "rb").read()
    return [i for i in range(len(content)) if content[i:i+2] == b'\xff\xd9']

def get_lsb_stats(path):
    img = Image.open(path).convert('RGB')
    data = np.array(img)
    lsb = data & 1
    return [np.mean(lsb[:,:,i]) for i in range(3)]

def chi_square_attack(path, block_size=1024):
    img = Image.open(path).convert('RGB')
    data = np.array(img).flatten()
    lsbs = data & 1
    num_blocks = len(lsbs) // block_size
    p_values = []
    for i in range(num_blocks):
        block = lsbs[i*block_size : (i+1)*block_size]
        obs = [np.sum(block == 0), np.sum(block == 1)]
        exp = [block_size / 2, block_size / 2]
        _, p = chisquare(obs, f_exp=exp)
        p_values.append(p)
    return np.mean(p_values)

print(f"{'Label':<15} | {'Size':<10} | {'MD5':<35} | {'EOI Count':<10} | {'LSB (R,G,B)':<30} | {'Chi-Square'}")
print("-" * 130)
for label, path in files.items():
    if os.path.exists(path):
        size = os.path.getsize(path)
        md5 = get_md5(path)
        eoi = get_eoi(path)
        lsb = get_lsb_stats(path)
        lsb_str = ", ".join([f"{x:.6f}" for x in lsb])
        chi = chi_square_attack(path)
        print(f"{label:<15} | {size:<10} | {md5:<35} | {len(eoi):<10} | {lsb_str:<30} | {chi:.6f}")
