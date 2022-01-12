from pprint import pprint

with open ('out.txt') as f:
    txt = f.read()
    txt = txt.split('#')
    pprint(txt)