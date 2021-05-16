from scapy.all import *
import binascii

sport = random.randint(60456)

# SYN
ip=IP(dst='52.28.255.56')
SYN=TCP(sport=sport,dport=1080,flags='S',seq=0)
SYNACK=sr1(ip/SYN)

# SYN-ACK
ACK=TCP(sport=sport, dport=1080, flags='A', seq=SYNACK.ack + 1, ack=SYNACK.seq + 1)
send(ip/ACK)

#binascii.unhexlify()
#del pkt[IP].chksum pkt[TCP].chksum
first_socks = TCP(sport=sport, dport = 1080, flags='PA', seq=SYNACK.ack+1, ack=SYNACK.seq + 1)
first_socks /= (b"\x5a\x01\xfe\xdd\x74\x9c\x2e")#"\x5a\x01\xfe\xdd\x74\x9c\x2e"

print(first_socks.show2())
first_ask = sr(ip/first_socks)