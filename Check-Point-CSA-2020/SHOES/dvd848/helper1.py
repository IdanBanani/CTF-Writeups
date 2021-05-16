import socket

class RemoteServer:
    BUFFER_SIZE = 4096

    def __init__(self, ip, port, verbose = False):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.verbose = verbose

    def __enter__(self):
        self.s.connect((self.ip, self.port))
        return self

    def __exit__(self, *args):
        self.s.close()

    def _print(self, prefix, msg):
        if self.verbose:
            print("{}{}".format(prefix, " ".join(["{:02x}".format(x) for x in msg])))

    def send(self, msg):
        self._print("Sending : ", msg)
        self.s.send(msg)

    def recv(self):
        msg = self.s.recv(self.BUFFER_SIZE)
        self._print("Received: ", msg)
        return msg