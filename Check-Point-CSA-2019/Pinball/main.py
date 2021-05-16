import os
import mmap
import string

from timeit import default_timer as timer




def memory_map(filename, access=mmap.ACCESS_READ):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDONLY)
    return mmap.mmap(fd, size, access=access)


class PinballCipher(object):
    def __init__(self, table_str):
        self.table = []  # [Y][X]
        for row in table_str.split("\n"):
            self.table.append([int(x) for x in row.split()])
        self.rows = len(self.table)
        self.columns = len(self.table[0])

    def initialize(self, py, px, vy, vx):
        assert (0 <= px < self.columns)
        assert (0 <= py < self.rows)
        assert (vx == 1 or vx == -1)
        assert (vy == 1 or vy == -1)

        self.py = py
        self.px = px
        self.vy = vy
        self.vx = vx
        self.reset = True

    def next(self):
        yield self.table[self.py][self.px]
        self.reset = False

        while not self.reset:
            expected_y = self.py + self.vy
            expected_x = self.px + self.vx

            #if reached border
            if expected_y < 0 or expected_y >= self.rows:
                self.vy *= -1
            if expected_x < 0 or expected_x >= self.columns:
                self.vx *= -1

            self.py += self.vy
            self.px += self.vx
            yield self.table[self.py][self.px]



table_str = """
177 030 077 225 170 116 089
228 139 058 083 195 202 201
197 113 114 053 184 105 043
178 029 210 090 150 045 212
135 240 099 051 147 085 060
156 039 169 101 078 180 165
075 108 102 163 166 027 092
204 046 015 198 209 086 120
232 172 106 154 226 023 057
054 141 216 149 153 142 071
""".strip()

start = timer()



with memory_map("msg.enc") as ciphertext:

# ...

# with open("msg.enc",'rb') as ciphertext:
#     ciphertext = ciphertext.read()

    ciphertext_len = len(ciphertext) #90
    pc = PinballCipher(table_str)

    for y in range(pc.rows):
        for x in range(pc.columns):
            for vy in [1, -1]:
                for vx in [1, -1]:
                    res = ""
                    pc.initialize(y, x, vy, vx)
                    for i, c in zip(range(ciphertext_len), pc.next()):
                        xored_c = chr(ciphertext[i] ^ c)
                        if xored_c not in string.printable:
                            break
                        res += xored_c
                    else:
                        print(res)
                        print((y, x, vy, vx))
                        print("\n")
fff = os.open("msg.enc", os.O_RDONLY)
ddd = os.open("msg.enc", os.O_RDONLY)
end = timer()
print(end - start)
#0.0009599999999999956
# 0.0008625999999999981