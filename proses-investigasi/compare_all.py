import os

files = [
    "Picture_UAS_Steganografi.jpg",
    "Picture_UAS_Steganografi_hidden.jpg",
    "Picture_UAS_Steganografi_fixnodata.jpg"
]

for f in files:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print(f"File: {f}")
        print(f"  Size: {size} bytes")
        with open(f, "rb") as img:
            content = img.read()
            eoi_index = content.find(b'\xff\xd9')
            if eoi_index != -1:
                print(f"  EOI at: {eoi_index}")
                extra = content[eoi_index+2:]
                print(f"  Extra bytes: {len(extra)}")
            else:
                print("  EOI NOT FOUND")
    else:
        print(f"File {f} not found.")
