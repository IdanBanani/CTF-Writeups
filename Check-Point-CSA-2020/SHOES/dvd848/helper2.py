import socket, os, re
import shoes

TCP_IP = '52.28.255.56'
TCP_PORT = 1080

KEY = bytes.fromhex("00 43 53 41") # \x00CSA

def xor(one, two):
    return bytes(a ^ b for (a, b) in zip(one, two))

def setup_connection(ip):
    s.send(shoes.ClientGreeting(version = shoes.SHOES_PROTOCOL_VERSION, auth_list = [shoes.SHOES_AUTH_TYPE_XOR]).to_bytes())

    challenge_msg =  shoes.ServerChoice.from_bytes(s.recv())
    
    s.send(shoes.ClientAuth(version = shoes.SHOES_PROTOCOL_VERSION, auth_data = xor(challenge_msg.auth_data, KEY)).to_bytes())
    
    s.send(shoes.ClientConnectionRequest(version = shoes.SHOES_PROTOCOL_VERSION, command = shoes.SHOES_COMMAND_ESTABLISH_TCP_IP,
                                         address = shoes.ipaddress.IPv4Address(ip), port = 80).to_bytes())

    server_response = shoes.ServerConnectionResponse.from_bytes(s.recv())

    if server_response.status != shoes.SHOES_STATUS_SUCCESS:
        raise Exception("Error setting up connection, status = {}".format(server_response.status))
    assert(server_response.status == shoes.SHOES_STATUS_SUCCESS)

with RemoteServer(TCP_IP, TCP_PORT, verbose=True) as s:    
    setup_connection("192.168.173.10")