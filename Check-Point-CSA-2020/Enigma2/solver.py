from pwn import *
import pprint


def help_me_skip(conn):
    skip = conn.recvlineS().rstrip()
    # if 'Encrypting' not in skip and 'understand' not in skip:
    print("skipped: ", skip)


if __name__ == "__main__":
    try:
        conn = remote('18.156.68.123', 80)
        help_me_skip(conn)
        help_me_skip(conn)
        server_str = """
  HELLO FIELD AGENT!
  COMMANDS:
      SEND-SECRET-DATA
      GET-SECRET-DATA
      GOODBYE
      """
        server_str = ''.join(list(c for c in server_str if c.isalpha()))
        # print(server_str)
        request = 'GET-SECRET-DATA'  # remainder 0-12
        request = request.replace('-', '')

        mapping = dict()
        remainder = 0
        for message_num in range(26):
            lines = conn.recvlinesS(5)
            if message_num == 0:
                secret_command = lines[3]

            print(lines)

            lines = ''.join(lines)
            lines = [c for c in lines if c.isalpha()]
            lines = ''.join(lines) #length 57

            # i : 0 - 56
            for i, c in enumerate(lines):
                #if you wish to send the letter server_str[i] at such a remainder-> expect c
                t = ((remainder, server_str[i]))
                if t not in mapping.keys():
                    mapping[t] = c
                remainder = (remainder + 1) % 26

            conn.sendline()
            # skip I dont understand you
            help_me_skip(conn)
            help_me_skip(conn)
            help_me_skip(conn)

        #last roatation - return to original message, remainder will be 5 now
        # but just if we don't send any capital letters
        #so we need remainder of 11 to be exactly - so lets send 1 empty message
        # and then one captial! letter
        lines = conn.recvlinesS(5) # these lines will be the same as the first ones ,meaning remainder is now 5
        print(lines)
        remainder = (remainder + len(server_str)) % 26 # remainder will be 5
        # print(lines)

        conn.sendline('A')
        help_me_skip(conn)
        help_me_skip(conn)
        help_me_skip(conn)
        lines = conn.recvlinesS(5) # remainder will now be 10
        print(lines)
        remainder = (remainder + len(server_str) + 1) % 26 # (5+57+1) % 26 = 11

        # print (remainder)
        code_word =''
        for c in request:
            code_word += mapping[remainder,c]
            remainder = (remainder + 1) % 26

        code_word = code_word[0:3]+'-'+str(code_word[3:9])+'-'+str(code_word[9:])

        conn.sendline(code_word)
        help_me_skip(conn)
        # help_me_skip(conn)
        # help_me_skip(conn)
        encrypted_flag = conn.recvlineS()

        decrypted_flag=''
        for c in encrypted_flag:
            if c.isalpha():
                for k,v in mapping.items():
                    if v == c:
                        if k[0] == remainder:
                            decrypted_flag += k[1]
                            remainder = (remainder + 1) %26
                            break
                else:
                    remainder = (remainder + 1) % 26
                    decrypted_flag += '*'
            else:
                decrypted_flag += c

        print(decrypted_flag)
        # conn.sendline(str(code[0:4])+'-'+str(code[4:10])+'-'+str(code[10:]))
        # my_flag = conn.recvlineS()
        # while my_flag != '\n':
        #     print(my_flag)
        #     my_flag = conn.recvlineS()

    finally:
        conn.close()
