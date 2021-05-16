#! /usr/bin/python3

import sys
import itertools
from hashlib import sha256
from Crypto.Cipher import ARC4

PROOF_OF_WORK_DIFFICULTY = 25 #bit

def proof_of_work(buf,n):
    i = 0
    while True:
        for prefix in itertools.product(range(0x30,0x7E), repeat = i):
            h = sha256()
            h.update(bytes(prefix))
            h.update(buf)
            if bin(int(h.hexdigest(),16)).endswith("0"*n):
                return prefix
        i += 1

def recover_flag(solution, e_flag):
    prow = proof_of_work(solution.encode("utf8"), PROOF_OF_WORK_DIFFICULTY)
    prow = bytes(prow).decode("utf8")
    key = f"RC4KEYFILLER|{solution}|{prow}"
    key = key.encode("utf8")
    return ARC4.new(key).decrypt(e_flag)


if __name__ == "__main__":
    solution = " ".join(sys.argv[1:])
    with open("flag.txt.enc","rb") as fh:
        e_flag = fh.read()
    flag = recover_flag(solution, e_flag)
    try: 
        flag = flag.decode("utf8")
        if flag.startswith("CSA"):
            print("Congratulations!")
            print("Your flag is: ", flag)
        else:
            print("Sorry, try again")
    except:
        print("Sorry, try again")

# python3 submit.py Germain scales Franklin abacus Curie telescope Lovelace pencil Noether laptop
