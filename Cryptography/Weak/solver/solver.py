from pwn import *
import jwt

long_name = "aaaaaaaaaaaaaaaaaaaaaaaaaaaa"
jwt_secret = "internet"
random_token = bytes(f"name={long_name};apalah", "utf-8")
target_token = b"name=admin;apalah"


def solve(cookie):
    decoded = jwt.decode(cookie, jwt_secret, algorithms=["HS256"])

    e, iv, rand = decoded["token"].split("+")
    xor_mask = bytes([a ^ b for a, b in zip(random_token[:16], target_token[:16])])
    iv = bytearray(bytes.fromhex(iv))
    for i in range(len(xor_mask)):
        iv[i] ^= xor_mask[i]

    admin_token = f"{e}+{iv.hex()}+{rand}"

    new_jwt = jwt.encode(
        {
            "name": "admin",
            "user_id": decoded["user_id"],
            "token": admin_token,
        },
        jwt_secret,
        algorithm="HS256",
    )

    return new_jwt


def pwn():
    r = remote("ctf.find-it.id", 7301)

    r.recvuntil(b"Enter your choice (1/2/3): ")
    r.sendline(b"1")

    r.recvuntil(b"Enter your name: ")
    r.sendline(bytes(long_name, "utf-8"))

    r.recvuntil(b"Store this cookie for login: ")
    cookie = r.recvline().strip()
    new_cookie = solve(cookie.decode())

    r.recvuntil(b"Enter your choice (1/2/3): ")
    r.sendline(b"2")

    r.recvuntil(b"Enter your name: ")
    r.sendline(b"admin")
    r.recvuntil(b"Enter your cookie: ")
    r.sendline(bytes(new_cookie, "utf-8"))

    r.recvuntil(b"GG, here your flag: ")
    flag = r.recvline().strip()
    print(flag.decode())


pwn()
