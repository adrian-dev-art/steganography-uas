from PIL import Image
import os

def create_super_clean(input_path, output_path):
    img = Image.open(input_path)
    # Re-saving without any metadata or original bitstream
    img.save(output_path, "JPEG", quality=95)
    print(f"Super clean image created at: {output_path}")

create_super_clean("Picture_UAS_Steganografi_fixnodata.jpg", "super_clean.jpg")
