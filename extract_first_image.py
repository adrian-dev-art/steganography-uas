import os

file_path = "Picture_UAS_Steganografi_hidden.jpg"
output_path = "first_image.jpg"

if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
        # Extract up to the first EOI marker (inclusive)
        first_image = content[:309134 + 2]
        with open(output_path, "wb") as out:
            out.write(first_image)
        print(f"First image (309136 bytes) saved to {output_path}")
else:
    print(f"File {file_path} not found.")
