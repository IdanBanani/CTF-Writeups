#!/usr/bin/python3
import socket
from pwn import *
from time import sleep
from zlib import crc32
from struct import pack



def get_crc32(msg):
        crc = crc32(msg)
        cutted = crc & 0xffffffff
        packed = pack(">I",cutted )
        # for p in packed:
        #         print (p,chr(p))
        return packed

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
        req = b"\x5a\x01\x00\x01\xc0\xa8\xad\x14\x00\x50" # 192.168.173.20: 80
        # req = b"\x5a\x01\x00\x01\xc0\xa8\xad\x0a\x00\x50" # 'HTTP/1.1 301 Moved Permanently to http://192.168.173.20F
        req+=get_crc32(req)
        conn.send(req)
        conn.recv(1024)
        send_http_req(conn)


def send_http_req(conn):
        req = b'''GET /Flag.jpg HTTP/1.1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36\r\nHost: www.tutorialspoint.com\r\nAccept-Language: en-us\r\nConnection: Keep-Alive\r\n\r\n'''


        conn.send(req)
        temp =conn.recvuntil(b'\r\n\r\n')
        print(temp)
        f = open('flag4.png', 'wb')

        added = 0
        while added < (80590 - 4096):
            a = conn.recv()
            # print(a)
            print(added)
            f.write(a)
            added += len(a)
        a = conn.recv(80590-added)
        f.write(a)

def main():
        host, port = "52.28.255.56", 1080
        conn = remote(host,port)
        init_conn(conn)
        get_http(conn)
        conn.close()


if __name__ == "__main__":
    main()

