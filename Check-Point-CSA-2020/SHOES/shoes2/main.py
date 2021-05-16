from scapy.all import *

# rdpcap comes from scapy and loads in our pcap file
packets = rdpcap('capture.pcapng')

# Let's iterate through every packet
packets = packets[63:86]
for i,packet in enumerate(packets):
    # We're only interested packets with a DNS Round Robin layer
    # if packet.haslayer(DNSRR):
        # If the an(swer) is a DNSRR, print the name it replied with.
        # if isinstance(packet.an, DNSRR):
    # if (packet.)
    # print(packet.show())
    print('----------------------', i ,'-------------------------')
    packet.show()