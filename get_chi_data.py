import numpy as np
from PIL import Image
from scipy.stats import chisquare
import os

def chi_square_attack(path, block_size=1024):
    if not os.path.exists(path): return 0
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

files = {
    "Suspect": "Picture_UAS_Steganografi.jpg",
    "Clean_WA": "Picture_UAS_Steganografi_fixnodata.jpg",
    "Super_Clean": "super_clean_baseline.jpg",
    "Steghide": "Picture_UAS_Steganografi_steghide.jpg",
    "OpenStego": "Picture_UAS_Steganografi_hidden.jpg"
}

print(f"{'File':<15} | {'Chi-Square P-Value'}")
print("-" * 35)
for label, path in files.items():
    p_val = chi_square_attack(path)
    print(f"{label:<15} | {p_val:.6f}")
