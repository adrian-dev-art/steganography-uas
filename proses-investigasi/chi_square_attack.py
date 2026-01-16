import numpy as np
from PIL import Image
from scipy.stats import chisquare

def chi_square_attack(path, block_size=1024):
    img = Image.open(path).convert('RGB')
    data = np.array(img).flatten()

    # We only care about the LSBs
    lsbs = data & 1

    # Divide into blocks and perform chi-square test on each
    num_blocks = len(lsbs) // block_size
    p_values = []

    for i in range(num_blocks):
        block = lsbs[i*block_size : (i+1)*block_size]
        # Count frequencies of 0 and 1
        obs = [np.sum(block == 0), np.sum(block == 1)]
        # Expected is 50/50 if it's random/encrypted data
        exp = [block_size / 2, block_size / 2]

        _, p = chisquare(obs, f_exp=exp)
        p_values.append(p)

    return np.mean(p_values)

files = {
    "Suspect": "Picture_UAS_Steganografi.jpg",
    "Clean": "super_clean_baseline.jpg",
    "Steghide": "Picture_UAS_Steganografi_steghide.jpg"
}

print(f"{'File':<15} | {'Chi-Square P-Value (Avg)':<25}")
print("-" * 45)
for label, path in files.items():
    p_val = chi_square_attack(path)
    print(f"{label:<15} | {p_val:.6f}")
