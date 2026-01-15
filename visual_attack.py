import numpy as np
from PIL import Image
import os

def extract_lsb_plane(input_path, output_path):
    img = Image.open(input_path).convert('RGB')
    data = np.array(img)

    # Extract LSB of the Red channel (often used for hiding)
    lsb_red = (data[:,:,0] & 1) * 255

    lsb_img = Image.fromarray(lsb_red.astype(np.uint8))
    lsb_img.save(output_path)
    print(f"LSB Plane saved to: {output_path}")

files = {
    "Suspect": "Picture_UAS_Steganografi.jpg",
    "Clean": "super_clean_baseline.jpg",
    "Steghide": "Picture_UAS_Steganografi_steghide.jpg"
}

for label, path in files.items():
    out = f"lsb_plane_{label.lower()}.png"
    extract_lsb_plane(path, out)
