# Flag CSA{we_all_need_mirrors}
import base64
import json
import string
from pprint import pprint

import requests

ROWS = 5
COLS = 8

boards= [
    #distance = 1
    [[1, 1, 2, 2, 3, 3, 4, 4], [5, 5, 6, 6, 7, 7, 8, 8], [9, 9, 10, 10, 11, 11, 12, 12],
     [13, 13, 14, 14, 15, 15, 16, 16], [17, 17, 18, 18, 19, 19, 20, 20]],

    [[1, 2, 1, 2, 3, 4, 3, 4], [5, 6, 5, 6, 7, 8, 7, 8], [9, 10, 9, 10, 11, 12, 11, 12],
     [13, 14, 13, 14, 15, 16, 15, 16], [17, 18, 17, 18, 19, 20, 19, 20]],

    [[1, 2, 3, 1, 2, 3, 4, 0], [6, 8, 7, 6, 4, 7, 9, 10], [11, 12, 13, 8, 9, 10, 14, 15],
     [13, 16, 11, 12, 14, 15, 17, 18], [19, 0, 0, 16, 17, 18, 19, 0]],

    [[1, 2, 3, 4, 5, 6, 7, 8],
     [9, 10, 11, 12, 9, 10, 11, 12],
     [13, 14, 15, 16, 13, 14, 15, 16],
     [17, 18, 19, 20, 17, 18, 19, 20],
     [1, 2, 3, 4, 5, 6, 7, 8]],

    [[1, 2, 3, 4, 5, 1, 2, 3], [5, 6, 7, 8, 9, 10, 6, 4], [9, 10, 11, 12, 13, 14, 7, 8],
     [13, 14, 15, 16, 17, 18, 11, 12], [17, 18, 0, 0, 0, 0, 15, 16]],

    [[1, 2, 0, 0, 0, 0, 1, 2], [3, 4, 0, 0, 0, 0, 3, 4], [5, 6, 0, 0, 0, 0, 5, 6], [7, 8, 0, 0, 0, 0, 7, 8],
     [9, 10, 0, 0, 0, 0, 9, 10]],

    [[1, 0, 0, 0, 0, 0, 0, 1], [5, 0, 0, 0, 0, 0, 0, 5], [10, 0, 0, 0, 0, 0, 0, 10], [7, 0, 0, 0, 0, 0, 0, 7],
     [20, 0, 0, 0, 0, 0, 0, 20]],

    [[1, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 2], [3, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 3]],

    [[1, 3, 0, 0, 0, 0, 0, 0],
     [2, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 1],
     [0, 0, 0, 0, 0, 0, 0, 2],
     [0, 0, 0, 0, 0, 0, 3, 0]]
]

command = 'http://memento.csa-challenge.com:7777/verifygame?level='
level = 1
tail = '&board='

d = {}
for c in string.ascii_lowercase + '_CSA{}':
    key= (ord(c)%9)+1
    if key not in d:
        d[key] = []
    d[key].append(c)

flag = [None for i in range(25)]
count = 0
while count<25:
    for level in range(0,25):
        if flag[level] != None:
            continue
        for j,board in enumerate(boards):
            b = base64.b64encode(json.dumps(board).encode('utf-8')).decode('utf-8')
            r = requests.get(command + str(level) +tail+b)
            if r.content == b'1':

                count+=1
                print(count)
                flag[level] = d[j+1]
                break
for x in flag:
    print (x)