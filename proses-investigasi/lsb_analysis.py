from PIL import Image
import numpy as np

def analyze_lsb(path):
    img = Image.open(path)
    data = np.array(img)

    # Get the LSB of each color channel
    lsb = data & 1

    # Calculate entropy or just check for patterns
    for i in range(3):
        channel_lsb = lsb[:,:,i]
        avg = np.mean(channel_lsb)
        print(f"Channel {i} LSB average: {avg:.4f}")
        # If avg is close to 0.5, it might be random data (encrypted/compressed)
        # If avg is close to 0 or 1, it's likely clean or very simple data

analyze_lsb("Picture_UAS_Steganografi.jpg")
print("-" * 20)
analyze_lsb("Picture_UAS_Steganografi_fixnodata.jpg")
