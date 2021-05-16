import zlib
import binascii
import re

with open('raven.pdf', 'rb') as f:
    all_bytes = f.read()
    all_bytes_hex = binascii.hexlify(all_bytes)
    all_bytes_hex_str = all_bytes_hex.decode('ascii')

# find matches for 'stream.......endstream''
res = re.findall('73747265616d0a(.*?)0a656e6473747265616d0a', all_bytes_hex_str)

dict = { i+1 : val  for i,val in enumerate(res) }
#

# goes through all the content objects specified in object 69
array = [20, 60, 48, 46, 40, 42, 17, 44, 35, 56, 9, 45, 4, 35, 41, 19, 36, 35, 55, 21, 52, 53, 13]
for index in array:
    value = dict.get(index)
    as_bytes_str = bytearray.fromhex(value)

    z = zlib.decompress(as_bytes_str)
    print(chr(z[37]), end='')