import os

files = ["Picture_UAS_Steganografi.jpg", "Picture_UAS_Steganografi_hidden.jpg"]

for f in files:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print(f"File: {f}")
        print(f"Size: {size} bytes")
        with open(f, "rb") as img:
            img.seek(-10, 2)
            last_bytes = img.read()
            print(f"Last 10 bytes: {last_bytes.hex(' ')}")
            # Check for JPEG EOI marker FF D9
            content = open(f, "rb").read()
            eoi_index = content.find(b'\xff\xd9')
            if eoi_index != -1:
                print(f"EOI (FF D9) found at index: {eoi_index}")
                extra_bytes = size - (eoi_index + 2)
                print(f"Bytes after EOI: {extra_bytes}")
                if extra_bytes > 0:
                    print(f"Potential hidden data found after EOI!")
            else:
                print("EOI marker NOT found!")
        print("-" * 20)
    else:
        print(f"File {f} not found.")
