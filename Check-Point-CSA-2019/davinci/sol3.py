from scapy.all import *
import binascii
import struct
import numpy as np
import matplotlib.pyplot as plt

packets = rdpcap('davinci.pcap')

absolute_x = 200  # arbitrary value
absolute_y = 200  # arbitrary value
points = []

for i in range(35, len(packets)):
    packet = raw(packets[i])[27:]  # leftover data
    if len(packet) != 4:  # ignore long data
        continue
    if packet[0] & 1 == 0: # ignore long data
        continue

    relative_x = packet[2]  # x
    relative_y = packet[3]  # y
    if relative_x > 127:  # making is signed
        relative_x = (256 - relative_x) * -1
    if relative_y > 127:  # making is signed
        relative_y = (256 - relative_y) * -1

    relative_y = relative_y * -1  # because axis is on top left and not bot left.

    absolute_x = absolute_x + relative_x
    absolute_y = absolute_y + relative_y

    if packet[1] & 1:
        points.append([absolute_x, absolute_y])

data = np.array(points)
absolute_x, absolute_y = data.T
plt.scatter(absolute_x, absolute_y)
plt.show()
