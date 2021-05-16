from pwn import *
from time import sleep
from zlib import crc32
from struct import pack


def get_crc32(msg):
    # Return a bytes object containing the values v1, v2, ...
    # packed according to the format string fmt.
    # The arguments must match the values required by the format exactly.
    # > - Little endian ,  I - unsigned int (usually 4 bytes)
    msg_crc32 = crc32(msg)
    val = msg_crc32 & 0xffffffff
    return pack(">I", val)


def init_conn(conn):
    msg = b'\x5a\x01\xfe'
    msg += get_crc32(msg)
    conn.send(msg)
    res = conn.recv(1024)[:-4]
    req = b'\x5a'
    key = b'\x00CSA'
    for i in range(4):
        req += bytes([res[2 + i] ^ key[i]])
    req += get_crc32(req)
    print(req)
    conn.send(req)


def get_http(conn):
    req = b"\x5a\x01\x00\x01\xc0\xa8\xad\x14\x00\x50"
    req += get_crc32(req)
    conn.send(req)
    conn.recv(1024)
    send_http_req(conn)


def send_http_req(conn):
    req = b'''GET /Flag.jpg HTTP/1.1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36\r\nHost: www.tutorialspoint.com\r\nAccept-Language: en-us\r\nConnection: Keep-Alive\r\n\r\n'''

    conn.send(req)
    conn.recvuntil(b'\r\n\r\n')
    f = open('flag3.jpg', 'wb')
    while True:
        a = conn.recv(1024)
        print(a)
        f.write(a)


def main():
    host, port = "52.28.255.56", 1080
    conn = remote(host, port)
    init_conn(conn)
    get_http(conn)


if __name__ == "__main__":
    main()
