# Caesar Cipher

## Author
mojitodev

## Description
Pada suatu malam, Tung Tung Tung Tung Sahur ingin mendatangi seorang pemuda yang tidak bangun sahur setelah dipanggil sahur sebanyak 3 kali, tetapi tidak nyaut. Masalahnya adalah pintu kamar pemuda tersebut terkunci dengan password tertentu, tetapi terdapat file `cipher.txt` yang tersimpan dalam flasdisk di dekatnya yang bisa digunakan untuk menemukan passwordnya. Bantulah Tung Tung Tung Tung sahur untuk menemukan passwordnya!

## Solution
1. Buka file `ciphertext.txt` untuk melihat teks yang sudah terenkripsi 
2. Buat python script `solver.py` dengan menerapkan brute-force Caesar Cipher dengan mencoba semua kemungkinan shift (0–25). Untuk setiap percobaan shift, cek apakah hasil dekripsi mengandung substring `FindIT{}`.  
4. Saat shift yang benar ditemukan, dekripsi lengkap akan terbaca sebagai berikut `FindIT{Hmmmm_1_R34lly_d0nt_kn0w_Th3_P4ssw0rd}`