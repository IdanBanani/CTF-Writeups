import string
import random
import time


def create_configuration():
    number_of_rotors = random.randrange(3, 6)
    rotates_amounts = [3, 5, 7, 11, 17, 19, 23]

    result = []
    for _ in range(number_of_rotors):
        rotor = "".join(random.sample(string.ascii_uppercase, 26))
        rotates_amount = random.choice(rotates_amounts)
        result.append([rotor, rotates_amount])
    return result


class StrongerEnigma:

    class Rotor:
        def __init__(self, configuration, rotate_amount):
            self.data = configuration
            self.rotate_amount = rotate_amount

        def rotate(self):
            self.data = self.data[self.rotate_amount:] + \
                self.data[:self.rotate_amount]

        def encrypt(self, char):
            char_idx = string.ascii_uppercase.index(char)
            encrypted = self.data[char_idx]
            self.rotate()
            return encrypted

        def decrypt(self, char):
            char_idx = self.data.index(char)
            decrypted = string.ascii_uppercase[char_idx]
            self.rotate()
            return decrypted

    def __init__(self):
        todays_configuration = create_configuration()

        self.rotors = []
        for d in todays_configuration:
            self.rotors.append(StrongerEnigma.Rotor(d[0], d[1]))

    def __encrypt_char(self, char):
        encrypted = char
        if char in string.ascii_uppercase:
            for r in self.rotors:
                encrypted = r.encrypt(encrypted)
        return encrypted

    def __decrypt_char(self, char):
        decrypted = char
        if char in string.ascii_uppercase:
            for r in reversed(self.rotors):
                decrypted = r.decrypt(decrypted)
        return decrypted

    def encrypt(self, message):
        encrypted_message = ""
        for char in message:
            encrypted_message += self.__encrypt_char(char)
        return encrypted_message

    def decrypt(self, message):
        decrypted_message = ""
        for char in message:
            decrypted_message += self.__decrypt_char(char)
        return decrypted_message


def send_interface(machine):
    to_send = """
HELLO FIELD AGENT!
COMMANDS:
    SEND-SECRET-DATA
    GET-SECRET-DATA
    GOODBYE
    """
    message = machine.encrypt(to_send)
    send(message)
    return message


def process_message(server_machine, message):
    decrypted = server_machine.decrypt(message)

    if decrypted == "GET-SECRET-DATA":
        flag = open("flag.txt", "rt").read()
        encrypted = server_machine.encrypt(flag)
        send(encrypted)
    elif decrypted == "SEND-SECRET-DATA":
        encrypted = receive()
        decrypted = server_machine.decrypt(encrypted)
        open("secrets.txt", "a+").write(decrypted)
    elif decrypted == "GOODBYE":
        send("See you next time")
        exit()
    else:
        send("I don't understand you")


def send(message):
    pass  # couldn't extract this part of code from the machine


def receive():
    pass  # couldn't extract this part of code from the machine


def doEngima():
    starting_session_seconds = time.time()
    send("Insecure channel. Encrypting with today's configuration..")
    machine = StrongerEnigma()

    while True:
        send_interface(machine)
        client_message = receive()
        process_message(machine, client_message)


doEngima()
