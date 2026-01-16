import os

file_path = "Picture_UAS_Steganografi_hidden.jpg"
output_path = "extracted_data.bin"

if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
        eoi_index = content.find(b'\xff\xd9')
        if eoi_index != -1:
            extra_data = content[eoi_index + 2:]
            if extra_data:
                print(f"Found {len(extra_data)} bytes of extra data.")
                with open(output_path, "wb") as out:
                    out.write(extra_data)
                print(f"Extracted data saved to {output_path}")

                # Try to identify the data
                print(f"First 16 bytes (hex): {extra_data[:16].hex(' ')}")
                try:
                    print(f"First 16 bytes (text): {extra_data[:16].decode('utf-8', errors='ignore')}")
                except:
                    pass
            else:
                print("No extra data found after EOI.")
        else:
            print("EOI marker not found.")
else:
    print(f"File {file_path} not found.")
