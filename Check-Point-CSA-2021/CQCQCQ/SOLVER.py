# LAST WORD IS STOP
# FROM MISTER PHILLIPS TO ALL AGENTS STOP
import string
from pprint import pprint
from random import choice
# FROMMISTERPHILLIPSTOALLAGENTSSTOPTHEFLAGISCSAOPENCURLYBRACKETSCLASSICUNDERSCORECRYPTOUNDERSCORESTRIKESUNDERSCOREBACKCLOSECURLYBRACKETSSTOP
#FLAG - CSA{CLASSIC_CRYPTO_STRIKES_BACK}
#GRID -GATEWYBCDFHIKLMNOPQRSUVXZ
#Keyword - "GATEWAY"
#Phillips Cipher

#contains all the ABC except J => matrix of size 5x5
t= '''HSVNN PBLMS XATWW PEBXT CRRCB MULAA LCDLO MGRKI
PALAC VXMUE CSWIK GVLQZ DALRC AACQT BZMYA EVSME
SIXDV CUWMS BLVSR BXGPQ FATUM MSAQV YMVKX QERVB
FLTSR ATSKE ERQBB XTE'''

# print(set(t))
t.replace('\n','')
t=t.split()
num_of_groups = len(t)
header = 'FROMMISTERPHILLIPSTOALLAGENTSSTOP'
# header =header.split()
# total_len = sum(len(s) for s in header)
# header =''.join(header)
total_len= len(header)
d={}
group=0
upper_letters= string.ascii_uppercase

for i, c in enumerate(header):



    if i!=0 and i%5 == 0:
        group+=1
        if group == 8:
            group = 0

    encoded = t[group][i%5]
    if header[i] not in d:
        d[header[i]] = []

    tup= ((group+1,encoded))
    if tup not in d[header[i]]:
        d[header[i]].append(tup)

d['S'].append(((3,'B')))

pprint(d)