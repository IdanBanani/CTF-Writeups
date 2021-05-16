import collections
import random

from ServerSide import slotmachine_dummy

FLAG_LEN = 38
flag = "0" * FLAG_LEN  # our machine Flag
remote_flag = [None] * FLAG_LEN # The real "Not-Known-Yet" CSA Flag

PRINTABLE = "123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
flag_length = len(flag)
SLOT_LENGTH = 10
NO_COINS = "No more coins! Goodbye."
NOT_ENOUGH_COINS = "You don't have enough coins!"
INVALID_COIN_NUMBER = "Coin number can't be negative"
INITIAL_COINS = 10

###########################################
class Slotmachine(object):
    def __init__(self):
        self.slots = [[i] + [random.choice(PRINTABLE) for i in range(SLOT_LENGTH)] for i in flag]
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
        return result


def main():
    slotmachine = Slotmachine()
    print("You have {} coins".format(slotmachine.total_coins))
    get_next_num = True
    ####################################################
    s = setup_remote()

    while get_next_num:
        coins = 0
        result = slotmachine.spin(coins)
        remote_result = remote_spin(s, coins)
        if "0" in result:
            start = 0
            slot_idx = result.find("0", start)
            while slot_idx >= 0:
                remote_flag[slot_idx] = remote_result[slot_idx]
                print("".join([c if c is not None else "?" for c in remote_flag]))
                if all(remote_flag):
                    print("".join(remote_flag))
                    return
                slot_idx = result.find("0", slot_idx + 1)


def setup_remote():
    # s = requests.session()
    # s.get("http://csa.bet")
    s = slotmachine_dummy.Slotmachine()
    return s


def remote_spin(s: slotmachine_dummy.Slotmachine, coins):
    # r = s.get("http://csa.bet/spin/?coins={}".format(coins))
    # j = json.loads(r.text)
    # return j["result"]
    return s.spin(coins) #return the result

if __name__ == '__main__':
    main()