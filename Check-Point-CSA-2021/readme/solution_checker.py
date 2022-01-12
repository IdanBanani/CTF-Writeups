from Crypto.Cipher import ARC4

def check_key(key, key_checker_data):
    """ returns True is the key is correct.
        Usage:
        check_key('{I_think_this_is_the_key}', key_checker_data)
    """
    return ARC4.new(("CSA" + key).encode()).decrypt(key_checker_data) == b'success'

key = '{hEY_th@T_l5_thE_9RE4T_p[ZZL3}'
with open('key_checker_data','rb') as checker:
    key_checker_data = checker.read()
    print(check_key(key,key_checker_data))