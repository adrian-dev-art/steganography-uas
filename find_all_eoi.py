import os

file_path = "Picture_UAS_Steganografi_hidden.jpg"

if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
        index = 0
        while True:
            index = content.find(b'\xff\xd9', index)
            if index == -1:
                break
            print(f"Found EOI (FF D9) at index: {index}")
            index += 2
else:
    print(f"File {file_path} not found.")
