from scapy.all import *
from scapy.layers.l2 import Ether
handshake1 = Ether(dst='52:54:00:12:35:02')/IP(dst='52.28.255.56',flags='DF')/TCP(dport=1080,flags='S',seq=1898442754, chksum=int('0x3f92',16), window=64240, options=[('WScale', 7),('MSS',1460),('SAckOK', ''),('NOP', None),('Timestamp', (2635348509, 0))] )
print(handshake1.show2())
SYNACK= srp(handshake1)

handshake2 = Ether()/IP(dst='52.28.255.56')/TCP(dport=1080,flags='A',seq=SYNACK.ack + 1, ack=SYNACK.seq + 1)
print(len(handshake2))
