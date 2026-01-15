import numpy as np
from PIL import Image
from scipy.stats import chisquare
import os

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

def spa_attack(path):
    img = Image.open(path).convert('L')
    data = np.array(img).flatten().astype(int)
    x = y = 0
    for i in range(len(data) - 1):
        u, v = data[i], data[i+1]
        if (v % 2 == 0 and u < v) or (v % 2 == 1 and u > v):
            if (u + v) % 2 == 0: x += 1
            else: y += 1
    if x + y == 0: return 0
    return max(0, (x - y) / (x + y))

files = {
    "Suspect": "Picture_UAS_Steganografi.jpg",
    "Clean": "super_clean_baseline.jpg",
    "Steghide": "Picture_UAS_Steganografi_steghide.jpg",
    "OpenStego": "Picture_UAS_Steganografi_hidden.jpg"
}

print(f"{'File':<15} | {'Chi-Square':<12} | {'SPA Rate':<10}")
print("-" * 45)
for label, path in files.items():
    if os.path.exists(path):
        chi = chi_square_attack(path)
        spa = spa_attack(path)
        print(f"{label:<15} | {chi:.6f} | {spa:.6f}")
