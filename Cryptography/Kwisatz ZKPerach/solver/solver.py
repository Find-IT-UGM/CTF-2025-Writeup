#!/usr/bin/env python3
import random
from math import gcd
from sympy import mod_inverse
from pwn import *
from randcrack import RandCrack

HOST = "103.127.138.252"
PORT = 4444

def solve():
    r = remote(HOST, PORT, level='debug')

    rc = RandCrack()
    
    gather_mode = True
    gather_finished = False
    gathered_count = 0
    needed_b = 78

    store_solve_data = None

    # 1) Parse n
    r.recvuntil(b"n = ")
    n_line = r.recvline().strip()
    n_val = int(n_line.decode(errors="ignore"))

    # 2) Parse y
    r.recvuntil(b"y = ")
    y_line = r.recvline().strip()
    y_val = int(y_line.decode(errors="ignore"))

    # 3) "Can you read my mind?" => "Your choice [1/2]:"
    r.recvuntil(b"Your choice [1/2]:")
    r.sendline(b"1")
    print("[SEND] 1 (enter 256-round loop)")

    rounds = 256
    for round_i in range(rounds):

        # (A) Possibly switch from gather to solve at round start
        if gather_finished and gather_mode:
            print(f"[ROUND {round_i}] We finished gathering in the previous round. Switching to solve mode now.")
            gather_mode = False

        # (B) "Give me an s:"
        r.recvuntil(b"Give me an s:")
        if gather_mode:
            while True:
                s_candidate = random.randrange(1, n_val)
                if gcd(s_candidate, n_val) == 1:
                    break
            our_s = s_candidate
            store_solve_data = None
        else:
            # Solve mode => predict next 256-bit b
            next_b_256 = rc.predict_getrandbits(256)  # or 8 rc.predict() calls
            b_mod_2 = next_b_256 % 2

            while True:
                z_candidate = random.randrange(1, n_val)
                if gcd(z_candidate, n_val) == 1:
                    break

            z_sq = pow(z_candidate, 2, n_val)
            y_inv = mod_inverse(y_val, n_val)
            if b_mod_2 == 1:
                our_s = z_sq
            else:
                our_s = (z_sq * y_inv) % n_val

            store_solve_data = (z_candidate, our_s, b_mod_2)

        r.sendline(str(our_s).encode())
        print(f"[ROUND {round_i}] Sent s = {our_s}")

        # (C) "Let's spin the gigantic roulette to determine your fate:"
        r.recvuntil(b"Let's spin the gigantic roulette to determine your fate:")
        while True:
            line_b = r.recvline(timeout=5)
            if not line_b:
                print("[ERROR] Timed out reading b.")
                return
            line_b_str = line_b.decode(errors="ignore").strip()
            if line_b_str.isdigit():
                big_b = int(line_b_str)
                print(f"[ROUND {round_i}] Got b = {big_b}")
                break

        if gather_mode:
            # Feed b to RandCrack
            tmp = big_b
            parts = []
            for _ in range(8):
                part = tmp & 0xffffffff
                parts.append(part)
                tmp >>= 32

            for p in parts:
                rc.submit(p)

            gathered_count += 1
            print(f"[INFO] Gathered b #{gathered_count}/{needed_b}")
            if gathered_count == needed_b:
                print(f"[ROUND {round_i}] Just gathered the 78th b. We'll skip verification this round, solve next round.")
                gather_finished = True

        # (D) "Are you ready to show me?" => "Your choice [1/2/3]:"
        r.recvuntil(b"Are you ready to show me?")
        r.recvuntil(b"Your choice [1/2/3]:")

        if gather_mode:
            # Still gathering => skip
            r.sendline(b"2")
            print(f"[ROUND {round_i}] Sent choice 2 (skip proof).")
            continue
        else:
            # Solve mode => do proof
            r.sendline(b"1")
            print(f"[ROUND {round_i}] Sent choice 1 (solve mode, do proof).")

            # (E) "Give me a z:"
            r.recvuntil(b"Give me a z:")
            if store_solve_data is None:
                z_dummy = random.randrange(1, n_val)
                r.sendline(str(z_dummy).encode())
                print("[WARN] store_solve_data was None, sent dummy z.")
            else:
                z_candidate, s_val, b_mod_2 = store_solve_data
                r.sendline(str(z_candidate).encode())
                print(f"[ROUND {round_i}] Sent z = {z_candidate}")

    # End of 256 rounds => read remainder
    rest = r.recvall(timeout=3)
    print(rest.decode(errors="ignore"))
    r.close()

def main():
    solve()

if __name__ == "__main__":
    main()
