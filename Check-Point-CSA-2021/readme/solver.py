import random
import string
from pprint import pprint
from Crypto.Cipher import ARC4

#This solution takes a lot of time (~5 minutes , about 3_355_706 iterations )
# {hEY_th@T_l5_thE_9RE4T_p[ZZL3}

def check_key(key, key_checker_data):
    """ returns True is the key is correct.
        Usage:
        check_key('{I_think_this_is_the_key}', key_checker_data)
    """
    return ARC4.new(("CSA" + key).encode()).decrypt(key_checker_data) == b'success'

d= {}
key_checker_data =b''
def solve():

    with open("messed.txt") as messed:
        mf = messed.read().replace('Â', '')
        # mf = messed.read().replace('\n', '')
        with open("plain.txt") as plain:
            global d
            p = plain.read()
            for i in range(len(p)):
                p_c = p[i]
                m_c = mf[i]
                if p_c.islower():
                    if p_c not in d:
                        d[p_c] = []
                    if m_c not in d[p_c]:
                        d[p_c].append(m_c)

        for c in string.printable:
            if c.lower() in d and c.lower() not in 'hey_that_is_the_great_puzzle':
                d.pop(c.lower())
        pprint(d)
        d['z'] = ['Z']
        options= 1
        for c in 'hey_that_is_the_great_puzzle':
            if c in d:
                options *= len(d[c])

        print(f'num of options {options}')

        with open('key_checker_data', 'rb') as checker:
            global key_checker_data
            key_checker_data = checker.read()

        solutions = set()
        while len(solutions) < 28_311_552:
            print(len(solutions))
            new_flag=[]
            flag = 'hey_that_is_the_great_puzzle'.split('_')
            for word in flag:
                new_word = ''
                for c in word:
                    new_c = random.choice(d[c])
                    new_word += new_c
                new_flag.append(new_word)

            new_flag = '{' + '_'.join(new_flag) + '}'

            if new_flag not in solutions:
                if (check_key(new_flag, key_checker_data)):
                    print(new_flag)
                    break
                else:
                    solutions.add(new_flag)

        print("finished")

solve()
