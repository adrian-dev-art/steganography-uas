from PIL import Image
import numpy as np
import os

def get_lsb_stats(path):
    img = Image.open(path)
    data = np.array(img)
    lsb = data & 1
    return [np.mean(lsb[:,:,i]) for i in range(3)]

# 1. Create Super Clean Baseline from the Clean Reference
img = Image.open("Picture_UAS_Steganografi_fixnodata.jpg")
img.save("super_clean_baseline.jpg", "JPEG", quality=100, subsampling=0)

# 2. Compare Suspect with Super Clean Baseline
suspect_lsb = get_lsb_stats("Picture_UAS_Steganografi.jpg")
baseline_lsb = get_lsb_stats("super_clean_baseline.jpg")

print("--- BASELINE COMPARISON ---")
print(f"Suspect LSB:  {suspect_lsb}")
print(f"Baseline LSB: {baseline_lsb}")
print(f"Difference:   {[abs(s - b) for s, b in zip(suspect_lsb, baseline_lsb)]}")

with open("baseline_comparison.txt", "w") as f:
    f.write(f"Suspect LSB:  {suspect_lsb}\n")
    f.write(f"Baseline LSB: {baseline_lsb}\n")
    f.write(f"Difference:   {[abs(s - b) for s, b in zip(suspect_lsb, baseline_lsb)]}\n")
