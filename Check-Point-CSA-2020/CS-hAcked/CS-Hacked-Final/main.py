import itertools
import time

from pwn import *
from Crypto.Cipher import ARC4


# Solution is : ('particularly', 'administration', 'a', 'as', 'I', 'environmental', 'about', 'across', 'ability', 'according')
# CSA{i_gu355_I_need_tO_ChN4GE_mY_encrYp71On}
# Took 8 minutes for sequential (non-parallel) solution
# improvement - choose a random solution (pre-shuffling) and run in parallel

def main():
    with open('words2.txt') as f, open('dictionary.txt') as d:
        content = f.readlines()
        lengths = [len(l.rstrip()) for l in content]

        words = d.readlines()
        words = [((len(w.rstrip()), w.rstrip())) for w in words]

        solutions = []
        for i, length in enumerate(lengths):
            count = 0
            ans = []
            for tup in words:
                if (tup[0] + 1) * 2 == length:
                    ans.append(tup[1])
                    count += 1

            solutions.append(ans)

        solutions = itertools.product(*solutions)

    for solution in solutions:

        try:
            cipher = ARC4.new(b'csa-mitm-key')
            conn = remote('3.126.154.76', 80)
            s = conn.recv().decode('utf-8')
            print(s, end='')
            s = conn.recv()
            print(cipher.decrypt(s).decode('utf-8'), end="")

            for word in solution:
                conn.send(cipher.encrypt(bytes(word + "\n", encoding="utf-8")))

            response = cipher.decrypt(conn.recv()).decode('utf-8')
            if response.find('No flag for you!') == -1:
                print(response)
                print(solution)
                break
        finally:
            conn.close()


if __name__ == "__main__":
    main()
