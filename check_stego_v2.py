import os

files = ["Picture_UAS_Steganografi.jpg", "Picture_UAS_Steganografi_hidden.jpg"]

for f in files:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print(f"File: {f}, Size: {size} bytes")
        with open(f, "rb") as img:
            content = img.read()
            eoi_index = content.find(b'\xff\xd9')
            if eoi_index != -1:
                extra = content[eoi_index+2:]
                print(f"  EOI at: {eoi_index}")
                print(f"  Extra bytes: {len(extra)}")
                if len(extra) > 0:
                    print(f"  First 32 extra bytes (hex): {extra[:32].hex(' ')}")
            else:
                print("  EOI NOT FOUND")

# Check if the extra data is a known file type
if os.path.exists("extracted_data.bin"):
    with open("extracted_data.bin", "rb") as f:
        header = f.read(4)
        if header.startswith(b'PK\x03\x04'):
            print("Extracted data is a ZIP file!")
        elif header.startswith(b'\x89PNG'):
            print("Extracted data is a PNG file!")
        elif header.startswith(b'\xff\xd8'):
            print("Extracted data is another JPEG file!")
        elif header.startswith(b'Rar!'):
            print("Extracted data is a RAR file!")
        else:
            print(f"Unknown header: {header.hex(' ')}")
