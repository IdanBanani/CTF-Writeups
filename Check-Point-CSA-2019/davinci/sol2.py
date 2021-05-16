from pkt_data import *
import matplotlib.pyplot as plt
import numpy as np


# The 4 leftover data are mouse packet bytes and seem to be:
# 1st byte: [ ? | ? | ? | ? | ? | Middle Btn? | Right Btn? | Left Btn ]
# 2nd byte: signed X movement
# 3rd byte: signed Y movement
# 4th byte: Scroll movement? Anyway always 0 in our case

LEFT_BTN = 0x1

def is_left_button(pkt):
	return pkt[28] & LEFT_BTN

def get_x_movement(pkt):
	x_mov = int(pkt[29])
	if x_mov > 127:
		x_mov = -1 * (256 - x_mov)
	return x_mov

def get_y_movement(pkt):
	y_mov = int(pkt[30])
	if y_mov > 127:
		y_mov = -1 * (256 - y_mov)
	return y_mov


# Translation of a
def get_key_row_1(x):
	if x < 200:
		return 'q'
	elif x < 250:
		return 'w'
	elif x < 300:
		return 'e'
	elif x < 400:
		return 'r'
	elif x < 500:
		return 't'
	elif x < 600:
		return 'y'
	elif x < 700:
		return 'u'
	elif x < 750:
		return 'i'
	elif x < 850:
		return 'o'
	else:
		return 'p'

def get_key_row_2(x):
	if x < 200:
		return 'a'
	elif x < 300:
		return 's'
	elif x < 400:
		return 'd'
	elif x < 500:
		return 'f'
	elif x < 550:
		return 'g'
	elif x < 600:
		return 'h'
	elif x < 700:
		return 'j'
	elif x < 800:
		return 'k'
	else:
		return 'l'

def get_key_row_3(x):
	if x < 250:
		return 'z'
	elif x < 300:
		return 'x'
	elif x < 400:
		return 'c'
	elif x < 500:
		return 'v'
	elif x < 600:
		return 'b'
	elif x < 700:
		return 'n'
	else:
		return 'm'

def get_key(x,y):
	if y < 50:
		return " "
	elif y < 150:
		return get_key_row_3(x)
	elif y < 250:
		return get_key_row_2(x)
	else:
		return get_key_row_1(x)

if __name__ == "__main__":

	# Plotting the mouse movement
	# ==========================================================================

	# Creation of the figure
	fig = plt.figure()
	ax = fig.add_subplot(111)

	#Starting position of (0,0)
	curr_pos = [0, 0]

	# Arrays to store the (x,y) positions of the mouse
	x_pos = []
	y_pos = []

	# Arrays to store the (x,y) positions of the clicks
	click_x_pos = []
	click_y_pos = []


	# Loop on all the packets
	for i in range(37,5575):
		if i in [116, 189, 305, 382, 487, 614, 811, 905, 1039, 1171, 1261, 1384, 1508, 1604, 1710, 1862, 1942,
		2058, 2146, 2244, 2330, 2402, 2501, 2600, 2712, 2792, 2905, 3040, 3131, 3224, 3317, 3464, 3558, 3671, 3777,
		3960, 4113, 4230, 4369, 4465, 4592, 4737, 4889, 4995, 5147, 5241, 5349, 5476]:
			continue
		curr_pkt = eval("pkt"+str(i))


		curr_pos[0] += get_x_movement(curr_pkt)
		curr_pos[1] -= get_y_movement(curr_pkt)


		if is_left_button(curr_pkt):
			click_x_pos.append(curr_pos[0])
			click_y_pos.append(curr_pos[1])


	ax.scatter(click_x_pos, click_y_pos, color="red")

	plt.show()

	# flag = ''

	# for i in range(len(click_x_pos)):
	# 	flag += get_key(click_x_pos[i], click_y_pos[i])
	# print(flag)

