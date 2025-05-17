def xor_decrypt(data: bytes, key: int) -> bytes:
    return bytes(b ^ key for b in data)


def main():

    with open("xor_madness.bin", "rb") as f:
        encrypted = f.read()

  
    for key in range(256):
        decrypted = xor_decrypt(encrypted, key)
        try:
            text = decrypted.decode('utf-8')
        except UnicodeDecodeError:
            continue

 
        if text.startswith("FindITCTF{") and text.endswith("}"):
            print(f"Key found : {key}")
            print(f"Flag       : {text}")
            return

    print("No valid key found.")

if __name__ == "__main__":
    main()
