#!/usr/bin/env python3
#FLAG: CSA{I_L1K3_THE_TW1ST_4T_THE_END}
import json
import random
import collections
import math
import requests

from pwn import *
from mt19937predictor import MT19937Predictor

predictor = MT19937Predictor()

FLAG_LEN = 32
flag=[None for _ in range(FLAG_LEN)]

#Flag is 32 chars

PRINTABLE = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+-/:.;<=>?@[]^_`{}"
NO_COINS = "NO MORE COINS! GOODBYE."
NOT_ENOUGH_COINS = "YOU DON'T HAVE ENOUGH COINS!"
INVALID_COIN_NUMBER = "COIN NUMBER CAN'T BE NEGATIVE"
INITIAL_COINS = 10


class Slotmachine(object):
    def __init__(self):
        seed = random.SystemRandom().getrandbits(64)  # Using SystemRandom is slow, use only for seed.
        self.randoms=set()
                                         # This is a random number generator object
        self.random = random.Random(seed)  # This will make sure no one messes with my seeds!

        #Every char of the flag has its own slot in the machine
        # slot contains all the alphabet
        self.slots = [list(PRINTABLE) for i in range(FLAG_LEN)]

        self.attempt_num = 0
        self.total_coins = INITIAL_COINS
        self.last_result = ""
        self.last_gamble = 0

    def get_prize(self):
        result = self.last_result
        prize = sum([x for x in collections.Counter(result).values() if x > 2])
        # prize = 1
        prize *= self.last_gamble
        self.total_coins += prize
        return prize

    #Grab every flag letter and put it in the beginning of its slot
    def prepend_flag(self):
        for i in range(FLAG_LEN):
            self.slots[i].remove(flag[i])
            self.slots[i] = [flag[i]] + self.slots[i]

    def check_invalid_input(self, coins):
        if self.total_coins <= 0:
            self.last_result = ""
            return NO_COINS
        if self.total_coins < coins:
            self.last_result = ""
            return NOT_ENOUGH_COINS
        if coins < 0:
            self.last_result = ""
            return INVALID_COIN_NUMBER
        return None

    # My cat wrote this function
    def choice(self):
        #pick a random element from each slot and append it to the result,
        # No shuffeling.....
        rand_num = format(self.random._randbelow((1 << (FLAG_LEN * len(f'{len(PRINTABLE) - 1:b}'))) - 1),
                          '#0%db' % (len(self.slots) * int(math.log(len(PRINTABLE), 2)) + 2))[2:]

        print(rand_num)
        # if rand_num in self.randoms:
        #     print(self.attempt_num,'SAME RANDOM!!!')
        # else:
        #     self.randoms.add(rand_num)

        result = ""
        j = 0
        for i in range(0, ending:= len(rand_num), steps:=len(f'{len(PRINTABLE) - 1:b}')):
            binary_selected = rand_num[i:i + len(f'{len(PRINTABLE) - 1:b}')]
            int_format = int(binary_selected,2)
            c = self.slots[j][int_format]
            # print(f"j={j} i={i} binary={binary_selected} int={int_format} c= {c} end={ending} step={steps}")
            result += c
            j += 1

        # print('---------------------------------------')
        return result

    def spin(self, coins):
        invalid_message = self.check_invalid_input(coins)

        #if input was invalid
        if invalid_message:
            return invalid_message.center(FLAG_LEN)

        self.last_gamble = coins
        self.total_coins -= coins

        #Interesting
        # if self.attempt_num == 200:
        #     self.prepend_flag()
        self.attempt_num += 1

        result = self.choice() #takes one char from each slot (random indexes)
        self.last_result = result
        return result


def main():
    remote_session = setup_remote()
    get_next_num = True
    count = 0
    while count<200:
        remote_result = remote_spin(remote_session,coins=1)
        num = 0
        for i in range(FLAG_LEN):
            if i != 0:
                num = num << 6
            c = remote_result[i]
            idx = PRINTABLE.index(c)
            num += idx
        predictor.setrandbits(num,192)
        count+=1

#DIDNT WORK!!!!
    # while count < 200:
    #     predictor.getrandbits(192)
    #     count += 1

    while True:
        remote_result = remote_spin(remote_session, coins=1)
        num = f'{predictor.getrandbits(192):0192b}'
        for i in range(FLAG_LEN):
            if num[i*6:i*6+6] == '0'*6:
                if flag[i] is None:
                    flag[i] = remote_result[i]
                print("".join([c if c is not None else "?" for c in flag]))
                if all(flag):
                    print("".join(flag))
                    return



def setup_remote():
    s = requests.session()
    s.get("http://slot-machine-reloaded.csa-challenge.com/")
    return s

def remote_spin(s, coins):
    r = s.get("http://slot-machine-reloaded.csa-challenge.com/spin/?coins={}".format(coins))
    j = json.loads(r.text)
    return j["result"]

if __name__ == "__main__":
    main()


