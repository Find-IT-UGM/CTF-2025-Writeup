# Weak

## Author
hilmo

## Description
Simple login. By the way, I think using a common secret is a bad idea 🗿

## Solution
### Check Challenge Behavior
After submitting a name, the challenge will return a JWT token. Based on the challenge description, the secret key for the JWT must be common. By brute-forcing with `rockyou.txt`, the secret is revealed to be `internet`.

### Change JWT Payload
The JWT must contain `"name":"admin"` in its payload. To achieve this, we can change the payload to `{"name":"admin"}` and sign it using `internet` as the secret key.

### Exploit the `pce` Function
The challenge checks if the `name` in `jwt.payload["name"]` and `jwt.payload["token"]` are the same. Let’s analyze the token generator function below:

```python
def pce(str):
    iv = get_random_bytes(16)

    spce = (
        f"name={str}_{prefix * random.randint(1, 100)};uid={random.randint(1,10000000)}"
    )
    bpce = bytes(spce, "utf-8")
    p = pad(bpce, 16)
    c = AES.new(secret2, AES.MODE_CBC, iv)
    e = c.encrypt(p)

    return f"{e.hex()}+{iv.hex()}"
```

The `pce` function simply returns the combined ciphertext and the IV as hex. We can use the IV to flip the bits of the ciphertext.

```python
    ...
    e, iv, rand = decoded["token"].split("+")
    xor_mask = bytes([a ^ b for a, b in zip(random_token[:16], target_token[:16])])
    iv = bytearray(bytes.fromhex(iv))
    for i in range(len(xor_mask)):
        iv[i] ^= xor_mask[i]
    ...
```

### Getting the Flag
Construct a new JWT based on the information above and simply send it.
