from pwn import *
from collections import Counter
import copy


def is_relevant(current, checked, num_matching_letters):
    common_counter = Counter(current) & Counter(checked)
    return len(common_counter) >= num_matching_letters


# read the words from the file:

done = False

while True:

    if done:
        break

    with open("words.txt", "r") as file:
        try:
            words = set(file.read().splitlines())
            s = remote('tricky-guess.csa-challenge.com', 2222)
            # waiting for the message to be recieved:
            temp = s.recv()
            # print(temp)
            temp = s.recv(10)
            # print(temp)
            for i in range(15):
                print('---------', i, '---------')
                guess = words.pop()
                s.sendline(guess)
                resp = s.recvlineS().rstrip()
                print('Set size: ', len(words))

                if len(resp) < 3:
                    for item in copy.copy(words):
                        if not is_relevant(guess, item, int(resp)):
                            words.remove(item)
                else:
                    print('special:', resp)
                    done = True
                    break

        finally:
            s.close()
