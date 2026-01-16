import os
import hashlib

file_suspect = "Picture_UAS_Steganografi.jpg"
file_clean = "Picture_UAS_Steganografi_fixnodata.jpg"

def get_file_info(path):
    if not os.path.exists(path):
        return None
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        content = f.read()
        md5 = hashlib.md5(content).hexdigest()
        eoi_index = content.find(b'\xff\xd9')
    return {"size": size, "md5": md5, "eoi": eoi_index, "content": content}

info_suspect = get_file_info(file_suspect)
info_clean = get_file_info(file_clean)

print(f"Comparison: {file_suspect} vs {file_clean}")
print(f"Suspect Size: {info_suspect['size']} bytes")
print(f"Clean Size:   {info_clean['size']} bytes")
print(f"Size Diff:    {info_suspect['size'] - info_clean['size']} bytes")

if info_suspect['md5'] == info_clean['md5']:
    print("MD5 Hashes match! The files are identical.")
else:
    print("MD5 Hashes differ. Analyzing differences...")

    if info_suspect['eoi'] != info_clean['eoi']:
        print(f"EOI markers differ: Suspect at {info_suspect['eoi']}, Clean at {info_clean['eoi']}")

    # Check if suspect is just clean + something at the end
    if info_suspect['content'].startswith(info_clean['content']):
        print("Suspect file contains the clean file plus extra data at the end!")
        extra = info_suspect['content'][len(info_clean['content']):]
        print(f"Extra data ({len(extra)} bytes): {extra.hex(' ')}")
    else:
        print("The files have different internal structures.")
