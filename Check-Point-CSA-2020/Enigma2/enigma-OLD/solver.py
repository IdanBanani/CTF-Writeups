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
        # answer = dict()
        # for j in range(len(request)):
        #     i = j
        #     for _ in range(26):

        #         if i % 26 < len(request) and server_str[i % len(server_str)] == request[i % len(request)]:
        #             # print(to_send[i % 57], '|flag index',
        #             #       i % 13, 'message#', i//57, '|offset in message:', i % 57)
        #             if i % 13 in answer:
        #                 if answer[i % len(request)][0] > i//len(server_str):
        #                     answer[i % len(request)] = ((i//len(server_str), i % len(server_str)))
        #             else:
        #                 answer[i % len(request)] = ((i//len(server_str), i % len(server_str)))

        #         i += 26

        # pprint.pprint(answer)

        mapping = dict()
        # code = [0] * 26
        # print(code)

        remainder = 0
        for message_num in range(25):
            buffer = []
            lines = conn.recvlinesS(5)
            # print(lines)
            lines = ''.join(lines)
            lines = [c for c in lines if c.isalpha()]
            lines = ''.join(lines)
            # print(lines, len(lines))
            # i : 0 - 56
        #     for i, c in enumerate(lines):
        #         t = ((remainder, c))
        #         if t not in mapping.keys():
        #             mapping[t] = server_str[i]
        #         remainder = (remainder + 1) % 26

        #     conn.sendline()
        #     # skip I dont understand you
        #     help_me_skip(conn)
        #     help_me_skip(conn)
        #     help_me_skip(conn)

        # for _ in range(22):
        #     conn.sendline()
        #     help_me_skip(conn)
        #     help_me_skip(conn)
        #     help_me_skip(conn)
        #     lines = conn.recvlinesS(5)

        # conn.sendline(str(code[0:4])+'-'+str(code[4:10])+'-'+str(code[10:]))
        # my_flag = conn.recvlineS()
        # while my_flag != '\n':
        #     print(my_flag)
        #     my_flag = conn.recvlineS()

    finally:
        conn.close()
