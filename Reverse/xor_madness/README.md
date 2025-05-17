# xor_madness

## Author
mojitodev

## Description
Bombombini Gusini adalah seorang mahasiswa tahun pertama jurusan Teknologi Informasi yang tengah mendalami cryptography dan malware analysis di mata kuliah Peretasan Beretika. Suatu hari, dosen memberikan tugas berupa sebuah binary file bernama `xor_madness.bin`. Katanya jika ia berhasil mendapatkan `"sesuatu"` dari binary file tersebut, maka ia akan langsung mendapatkan nilai A. Bantulah ia untuk bisa mendapatkan `"sesuatu"` tersebut.

## Solution
1. Membuat script Python (`solver.py`) untuk mengaplikasikan XOR operation untuk mendapatkan flagnya dengan brute-force dan kunci 0.

2. Setelah menemukan kunci yang menghasilkan prefix yang valid, hentikan brute-force dan cetak kunci beserta flag yang terdekripsi.

Kunci yang benar adalah `0`, sehingga operasi XOR dengan kunci 0 tidak mengubah data, dan menghasilkan flag asli:

```python
def xor_decrypt(data, key):
    return bytes([b ^ key for b in data])

with open("xor_madness.bin", "rb") as f:
    encrypted = f.read()

for key in range(256):
    dec = xor_decrypt(encrypted, key)
    if dec.startswith(b"FindITCTF{"):
        print(f"Key ditemukan: {key}")
        print(f"Flag: {dec.decode()}")
        break
