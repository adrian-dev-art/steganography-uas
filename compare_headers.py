file1 = "Picture_UAS_Steganografi.jpg"
file2 = "Picture_UAS_Steganografi_fixnodata.jpg"

with open(file1, "rb") as f1, open(file2, "rb") as f2:
    b1 = f1.read(256)
    b2 = f2.read(256)

print(f"Header comparison (first 256 bytes):")
if b1 == b2:
    print("Headers are identical.")
else:
    print("Headers differ.")
    for i in range(min(len(b1), len(b2))):
        if b1[i] != b2[i]:
            print(f"First difference at offset {i}: {hex(b1[i])} vs {hex(b2[i])}")
            break

# Search for strings in the suspect file
import re
with open(file1, "rb") as f:
    content = f.read()
    strings = re.findall(b"[A-Za-z0-9]{4,}", content)
    print(f"Found {len(strings)} strings in suspect file.")
    # Print strings that look suspicious
    for s in strings:
        if b"flag" in s.lower() or b"key" in s.lower() or b"pass" in s.lower():
            print(f"Suspicious string: {s}")
