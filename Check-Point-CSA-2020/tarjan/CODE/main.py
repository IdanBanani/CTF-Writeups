# import matplotlib.pyplot as plt
# import networkx as nx
from collections import Counter
import re


def decimalToBinary(n):
    return bin(n).replace("0b", "")


edges = [[9459011, 9459014], [8834567, 8834570], [16484715, 16484718], [10536999, 10537002], [5360200, 5360202], [9219552, 9219554], [12180815, 12180822], [6840232, 6840234], [9045060, 9045061], [11177208, 11177209], [11759735, 11759737], [14370512, 14370514], [5040815, 10081638], [14104364, 14104365], [5298400, 5298401], [520991, 520993], [4762656, 4762657], [3424404, 3424406], [1955787, 15646330], [15455827, 15455830], [16176083, 16176085], [16746452, 16746453], [5806147, 1451538], [8531676, 8531678], [
    847235, 6777909], [13936711, 13936714], [4484468, 4484470], [1783775, 1783777], [1515704, 757854], [1362647, 1362650], [9927216, 9927217], [12178935, 12178938], [15606523, 15606526], [8906755, 8906758], [3688248, 3688249], [13860120, 13860121], [7669927, 7669929], [11053915, 11053917], [10777908, 2694478], [12786419, 3196605], [13042600, 13042602], [15378273, 7689137], [15287808, 15287810], [1187667, 1187670], [5977260, 5977261], [8324863, 8324866], [1255851, 10046834], [2811044, 2811046]]

# print(len(edges))
# for i, e in enumerate(edges):
#     x, y = e
#     if (abs(x - y) > 10):
#         r2 = ''
#         if(x > y):
#             reverse = 'Rev'
#             z = x
#             x = y
#             y = z

#         else:
#             reverse = ''
#         print(y/x)
#         if (abs(y - x*2)) < 1000:
#             if (y < x*2):
#                 r2 = 'minus'
#             xor_str = decimalToBinary(y ^ x*2)
#             print(f'index = {i}, x*2 ={x*2}, y={y} , xor = ',
#                   '0'*(6-len(xor_str)), xor_str, reverse, r2)
#         elif abs(y - x*4) < 1000:
#             if y < x*4:
#                 r2 = 'minus'
#             xor_str = decimalToBinary(y ^ x*4)
#             print(
#                 f'index = {i} , x*4 ={x*4}, y={y} , xor=', '0'*(6-len(xor_str)), xor_str, reverse, r2)
#         else:
#             if (y < x*8):
#                 r2 = 'minus'
#             xor_str = decimalToBinary(y ^ x*8)
#             print(
#                 f'index = {i} ,x*8 ={x*8}, y={y} , xor = ', '0'*(6-len(xor_str)), xor_str, reverse, r2)


with open('tree.txt') as f:

    dirty = f.readline()
    pattern = re.compile('[\W_]+')
    clean = pattern.sub('', dirty)
    clean = clean.lower()
    l = len(clean)
    print(l)
    final = []
    for i in range(l):
        final.append(clean[i:i+4])

    cnt = Counter(final)
    # result = re.sub('[^0-9]', '', dirty)
    print(cnt)
    # chars = []
    # words = []
    # new_edges = [(10081630, 10081638), (15646296, 15646330), (5806147, 5806152), (6777880, 6777909), (1515704,
    #                                                                                                   1515708), (10777908, 10777912), (12786419, 12786420), (15378273, 15378274), (10046808, 10046834)]
    # for edge in new_edges:
    #     x, y = edge
    #     chars.append((dirty[x], dirty[y]))
    # words.append(dirty[x:y+1])


# for c in chars:
#     print(c)

# for w in words:
#     print(w)

# G = nx.Graph()
# G.add_edge(chars)
# H = nx.DiGraph(G)

# plt.subplot(111)

# nx.draw(G, with_labels=True, font_weight='bold')
# plt.show()
