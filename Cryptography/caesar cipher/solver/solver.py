import string

def caesar_decrypt(ciphertext, shift):
    alphabet = string.ascii_lowercase
    result = []
    for ch in ciphertext:
        if ch.lower() in alphabet:
            idx = alphabet.index(ch.lower())
            dec = alphabet[(idx - shift) % 26]
            result.append(dec.upper() if ch.isupper() else dec)
        else:
            result.append(ch)
    return ''.join(result)


def main():
    
    with open('ciphertext.txt', 'r') as f:
        text = f.read()

    shift = 5  
    plain = caesar_decrypt(text, shift)

    print(f"[+] Shift = {shift}")
    print("Decrypted:", plain)

if __name__ == "__main__":
    main()
