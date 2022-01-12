from pwn import *
import base64
rot13 = str.maketrans(
    'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
    'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm')

xor_key = b'CC55AA'
t =b'WFKZLTABVKWVLXGMASVPYVP2ZRTKVHKV6XGBJKVEKX44YCVKXBK4XTBDVKSVL2WMACVLOVPEZQJ2VHCV'

t = base64.b32decode(t)


req=[]
for j in range(len(t)//len(xor_key)):
    for i in range(len(xor_key)):
        req.append(t[j*len(xor_key) + i] ^ xor_key[i])

req = ''.join([chr(v) for v in req])
print([ord(c) for c in req])
