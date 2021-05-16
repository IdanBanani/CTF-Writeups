#!/usr/bin/python3


import random
import collections
import requests


# from .secret import flag
# flag = 'CSA{JuST_1ik3_LeOn4rdO_d4_ViNc1}'
# flag = 'A' * 38
flag = [chr(i) for i in range(128, 166)]
# flag = ['C', 'S' ,' A'] + [chr(i) for i in range(131, 166)]


PRINTABLE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
flag_length = len(flag)
SLOT_LENGTH = 10
NO_COINS = "No more coins! Goodbye."
NOT_ENOUGH_COINS = "You don't have enough coins!"
INVALID_COIN_NUMBER = "Coin number can't be negative"
INITIAL_COINS = 10

class Slotmachine(object):
    def __init__(self):
        self.slots = [[i]+[random.choice(PRINTABLE) for i in range(SLOT_LENGTH)] for i in flag]
        self.attempt_num = 0
        self.total_coins = INITIAL_COINS
        self.last_result = ""
        self.last_gamble = 0

    def get_prize(self):
        result = self.last_result
        prize = sum([x for x in collections.Counter(result).values() if x > 2])
        prize *= self.last_gamble
        self.total_coins += prize
        return prize

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

    def spin(self, coins):
        invalid_message = self.check_invalid_input(coins)
        if invalid_message:
            return invalid_message.center(flag_length, ' ')

        self.last_gamble = coins
        self.total_coins -= coins

        random.seed(coins + self.attempt_num)
        self.attempt_num += 1

        for i in self.slots:
            random.shuffle(i)

        result = ""
        for i in self.slots:
            result += random.choice(i)
        self.last_result = result

        indexes = []
        for index, c in enumerate(result):
            # if c in 'A':
            if ord(c) >= 128:
                indexes.append(index)
        # print result
        return result, indexes


# This is used to run the slotmachine locally, the server doesn't use this.
# def main():
#     slotmachine = Slotmachine()
#     print("You have {} coins".format(slotmachine.total_coins))
#     get_next_num = True
#     while get_next_num:
#         try:
#             prize = 0
#             coins = int(input("Enter number of coins:\n"))
#             result = slotmachine.spin(coins)
#             if result == NO_COINS:
#                 get_next_num = False
#             elif result != NOT_ENOUGH_COINS:
#                 prize = slotmachine.get_prize()
#             print(result)
#             print("You won {} coins!".format(prize))
#             print("{} coins left.".format(slotmachine.total_coins))
#
#         except ValueError:
#             get_next_num = False
#         except NameError:
#             get_next_num = False


def main():
    correct_indexes_mapping = {}
    real_flag = ['C', 'S' , 'A' , '{'] + ['\x80'] * 33 + ['}']
    # recovered = ['C', 'S', 'A', '{', 'D', '0', 'n', "'", 't', '_', 'G', '4', 'm', 'b', 'l', '3', '_', 'W', '1', 't', 'h', '_', 'y', 'o', 'u', 'R', '_', 'p', 'R', 'n', 'G', '_', 'S', 'e', 'e', 'D', '5', '}']

    slotmachine = Slotmachine()
    for i in range(1, 40):
    # for i in range(1, 11):  # max coins = 10
        # slotmachine = Slotmachine()
        result, indexes = slotmachine.spin(i)
        correct_indexes_mapping[i] = indexes
        print ('result is: {0}'.format(result))
        slotmachine.get_prize()

    # print ()
    csa_session = requests.session()
    csa_session.get("http://csa.bet/")
    for i in range(1, 40):
    # for i in range(1, 11):  # max coins = 10
    #     csa_session = requests.session()
    #     csa_session.get("http://csa.bet/")
        csa_request = csa_session.get("http://csa.bet/spin/?coins=" + str(i))
        # print(csa_request.json())
        result = csa_request.json()['result']
        current_coins = csa_request.json()['current_coins']
        print ('{0} , {1}'.format(result, current_coins))

        for index in correct_indexes_mapping[i]:
            real_flag[index] = result[index]
            # print 'index = {0}, value = {1}'.format(index, result[index])
        # csa_session.cookies.clear() # similar to refreshing the page at the browser

    print (''.join(real_flag))


if __name__ == '__main__':
    main()