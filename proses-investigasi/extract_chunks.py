import os

file_path = "Picture_UAS_Steganografi_hidden.jpg"

if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        content = f.read()

        # Chunk 1: Between EOI 1 and EOI 2
        chunk1 = content[309134 + 2 : 987542]
        with open("chunk1.bin", "wb") as out:
            out.write(chunk1)
        print(f"Chunk 1 (678406 bytes) saved. Header: {chunk1[:16].hex(' ')}")

        # Chunk 2: After EOI 2
        chunk2 = content[987542 + 2 :]
        with open("chunk2.bin", "wb") as out:
            out.write(chunk2)
        print(f"Chunk 2 (452510 bytes) saved. Header: {chunk2[:16].hex(' ')}")

        # Check for common signatures in chunks
        signatures = {
            b"\xff\xd8\xff": "JPEG",
            b"\x89PNG\x0d\x0a\x1a\x0a": "PNG",
            b"PK\x03\x04": "ZIP",
            b"Rar!": "RAR",
            b"7z\xbc\xaf\x27\x1c": "7Z"
        }

        for name, chunk in [("Chunk 1", chunk1), ("Chunk 2", chunk2)]:
            for sig, sig_name in signatures.items():
                if sig in chunk:
                    print(f"Found {sig_name} signature in {name} at offset {chunk.find(sig)}")
else:
    print(f"File {file_path} not found.")
