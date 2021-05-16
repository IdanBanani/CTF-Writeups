import zlib
from scapy.all import *
# import binascii
from scapy.layers.inet import IP, TCP
from pwn import *
sport = 60456

# SYN
ip=IP(dst='52.28.255.56')
SYN=TCP(sport=sport,dport=1080,flags='S',seq=0,window = 64240)
# SYN=TCP(sport=sport,dport=1080,flags='S',seq=0,window = 64240,chksum='3f92')
SYNACK=sr1(ip/SYN)
# SYNACK.display()
# SYN-ACK
ACK=TCP(sport=sport, dport=1080, flags='A', seq=1, ack= 1)
send(ip/ACK)



#binascii.unhexlify

conn =remote('52.28.255.56',1080)

try:
    conn.send(b"\x5a\x01\xfe\xfe\xfe\xfe\x9A\x9A\xFF\xF0")
    reply =  conn.recv()
    for c in reply:
        print(hex(c),end=' ')
    print()

    next_request =bytearray(b"\x5a")

    to_xor = reply[3:6]
    xors = '43 53 41'
    xors = bytearray.fromhex(xors)
    one_xor_two = bytes(a ^ b for (a, b) in zip(to_xor, xors))

    # next_request = b"\x5a" + hex(a)
    next_request.append(reply[2])
    next_request.extend(one_xor_two)
    chksum = zlib.crc32(next_request).to_bytes(4,'little')
    next_request.extend(chksum[::-1])

    for c in next_request:
        print(hex(c),end=' ')
    print()

    # conn.send(next_request)
    # conn.send(bytes(next_request))

    ACK = TCP(sport=sport, dport=1080, flags='A', seq=8, ack=11)
    send(ip / ACK)

    reply =  conn.recv()
    print(reply)

finally:
    conn.close()