import base64

mdict = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
         'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
         's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']


def trans(a):
    if a == '=':
        return a
    ia = mdict.index(a)
    ia = 63 - ia
    return mdict[ia]


inp = open("ciphertext")
outp = open('solved.txt', 'w')
cipher_txt = inp.read()
outt = ""

for a in cipher_txt:  # aout:
    outt += trans(a)
outp.write(str(base64.b64decode(outt)))


