import hashlib
import os

files = [
    'Picture_UAS_Steganografi.jpg',
    'Picture_UAS_Steganografi_fixnodata.jpg',
    'super_clean_baseline.jpg',
    'Picture_UAS_Steganografi_steghide.jpg',
    'Picture_UAS_Steganografi_hidden.jpg'
]

print(f"{'Filename':<40} | {'Size':<10} | {'MD5'}")
print("-" * 85)
for f in files:
    if os.path.exists(f):
        size = os.path.getsize(f)
        md5 = hashlib.md5(open(f, "rb").read()).hexdigest()
        print(f"{f:<40} | {size:<10} | {md5}")
