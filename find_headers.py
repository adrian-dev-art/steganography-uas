import os

file_path = "Picture_UAS_Steganografi_hidden.jpg"

signatures = {
    b"\xff\xd8\xff": "JPEG",
    b"\x89PNG\x0d\x0a\x1a\x0a": "PNG",
    b"PK\x03\x04": "ZIP",
    b"Rar!": "RAR",
    b"7z\xbc\xaf\x27\x1c": "7Z",
    b"\x1f\x8b\x08": "GZIP",
    b"BZh": "BZIP2",
    b"%PDF": "PDF"
}

if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
        for sig, name in signatures.items():
            index = 0
            while True:
                index = content.find(sig, index)
                if index == -1:
                    break
                print(f"Found {name} signature at index: {index}")
                index += 1
else:
    print(f"File {file_path} not found.")
