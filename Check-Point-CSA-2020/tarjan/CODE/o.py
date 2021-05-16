from collections import Counter
outf = open('out.txt', 'w')

with open('aaa.txt') as f:
    lines = f.readlines()
    cc = Counter([*line for line in lines])
    print(cc)
    # new_lines = []
    # for line in lines:
    #     words = line.split(' ')

    # print(words)
    # new_words = list(filter(lambda a: a != 'fa00' and a != '00fa', words))
    # new_l = ' '.join(new_words)
    # new_lines.append(new_l)

    outf.writelines(new_lines)
    # counts = Counter(new_w)
    # print(counts)
    # print(txt.decode('cp1252'))
    # new_str = [c for c in txt if c.isalnum()]
    # new_str = bytearray.fromhex(txt).decode()
    # print(''.join(new_str))
