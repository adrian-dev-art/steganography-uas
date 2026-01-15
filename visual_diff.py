import numpy as np
from PIL import Image, ImageDraw
import os

def get_lsb_plane(path):
    if not os.path.exists(path): return None
    img = Image.open(path).convert('RGB')
    data = np.array(img)
    return data[:,:,0] & 1

def compare_and_mark(path_ref, path_target, label_target, output_path):
    lsb_ref = get_lsb_plane(path_ref)
    lsb_target = get_lsb_plane(path_target)

    if lsb_ref is None or lsb_target is None:
        print(f"Skipping {label_target}: File not found.")
        return

    # Ensure same shape
    if lsb_ref.shape != lsb_target.shape:
        print(f"Skipping {label_target}: Shape mismatch.")
        return

    diff = (lsb_ref != lsb_target)

    # Create visualization
    # We use the target image's LSB plane as background and mark differences
    base_img = Image.fromarray((lsb_target * 255).astype(np.uint8)).convert('RGB')
    draw = ImageDraw.Draw(base_img)

    height, width = diff.shape
    step = 16 # Finer blocks for better marking

    diff_count = 0
    for y in range(0, height, step):
        for x in range(0, width, step):
            block = diff[y:y+step, x:x+step]
            if np.any(block):
                draw.rectangle([x, y, x+step, y+step], outline="red", width=1)
                diff_count += 1

    base_img.save(output_path)
    print(f"Comparison [Suspect vs {label_target}]: {diff_count} blocks marked. Saved to {output_path}")

# Files
ref = "Picture_UAS_Steganografi.jpg" # Suspect as Reference
targets = {
    "Clean": "Picture_UAS_Steganografi_fixnodata.jpg",
    "Steghide": "Picture_UAS_Steganografi_steghide.jpg",
    "OpenStego": "Picture_UAS_Steganografi_hidden.jpg",
    "SuperClean": "super_clean_baseline.jpg"
}

print("--- VISUAL DIFFERENCE ANALYSIS (SUSPECT AS REFERENCE) ---")
for label, path in targets.items():
    out_name = f"diff_suspect_vs_{label.lower()}.png"
    compare_and_mark(ref, path, label, out_name)
