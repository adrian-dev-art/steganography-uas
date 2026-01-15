def xor_with_key(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

with open("extracted_data.bin", "rb") as f:
    data = f.read(1000)

key = b"password"
decrypted = xor_with_key(data, key)

print(f"Decrypted (first 64 bytes hex): {decrypted[:64].hex(' ')}")
print(f"Decrypted (first 64 bytes text): {decrypted[:64].decode('utf-8', errors='ignore')}")

# Try other common keys
keys = [b"password", b"PASSWORD", b"steganografi", b"forensic"]
for k in keys:
    dec = xor_with_key(data, k)
    if b"flag" in dec.lower() or b"http" in dec.lower() or b"PK" in dec[:4]:
        print(f"Found something with key: {k}")
        print(dec[:100])
