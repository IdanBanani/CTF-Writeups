# shoes.py

from ctypes import *
import binascii, ipaddress

SHOES_PROTOCOL_VERSION = 0x5A
SHOES_AUTH_TYPE_XOR = 0xFE
SHOES_ADDRESS_TYPE_IPV4 = 0x1
SHOES_COMMAND_ESTABLISH_TCP_IP = 0x1
SHOES_STATUS_SUCCESS = 0x0

class ShoesStruct(BigEndianStructure):
    _pack_ = 1
    CHECKSUM_LENGTH = 4

    def to_bytes(self, include_checksum = True):
        res = bytes(self)
        if include_checksum:
            res += self.calculate_checksum(res)
        return res

    @classmethod
    def from_bytes(cls, buf, callback = None):
        buf_without_checksum, checksum = cls.split_checksum(buf)
        obj = cls.from_buffer_copy(buf_without_checksum)
        initial_len = len(obj.to_bytes(include_checksum = False))

        if callback:
            obj = callback(obj, buf_without_checksum, initial_len)

        calc_checksum = cls.calculate_checksum(obj.to_bytes(include_checksum = False))

        if (checksum != calc_checksum):
            raise ValueError("Calculated checksum (0x{}) different from provided checksum (0x{})"
                                .format(calc_checksum.hex(), checksum.hex()))

        return obj


    @classmethod
    def split_checksum(cls, buf):
        if len(buf) < cls.CHECKSUM_LENGTH:
            raise ValueError("Provided buffer too short to contain checksum")
        buf_without_checksum = buf[:-1 * cls.CHECKSUM_LENGTH]
        checksum = buf[-1 * cls.CHECKSUM_LENGTH:]

        return (buf_without_checksum, checksum)

    @classmethod
    def calculate_checksum(cls, buf):
        return binascii.crc32(buf).to_bytes(cls.CHECKSUM_LENGTH, byteorder='big')



class ClientGreeting(ShoesStruct):
    _fields_ = [('version', c_uint8),
                ('num_auth', c_uint8)]
    _auth_list = (c_ubyte * 0)()

    def __init__(self, version = None, auth_list = None):
        super().__init__()
        if version is not None:
            self.version = version
        if auth_list is not None:
            self.auth_list = auth_list

    @property
    def auth_list(self):
        return list(bytes(self._auth_list))

    @auth_list.setter
    def auth_list(self, auth_list):
        self.num_auth = len(auth_list)
        self._auth_list = (self._auth_list._type_ * len(auth_list))()
        al = bytes(auth_list)
        assert(len(al) == len(auth_list))
        memmove(self._auth_list, al, len(auth_list))

    @classmethod
    def from_bytes(cls, buf):
        try:
            def handle_auth_list_callback(obj, buf_without_checksum, initial_len):
                if len(buf_without_checksum) != initial_len:
                    obj.auth_list = buf_without_checksum[initial_len:]
                if (len(obj._auth_list) != obj.num_auth):
                    raise ValueError("Declared number of authentication methods does not match provided number")
                return obj

            obj = super().from_bytes(buf, handle_auth_list_callback)
            return obj
        except Exception:
            raise

    def to_bytes(self, include_checksum = True):
        res = super().to_bytes(include_checksum = False) + memoryview(self._auth_list)
        if include_checksum:
            res += self.calculate_checksum(res)
        return res

from abc import ABC, abstractmethod, ABCMeta
class ShoesAuthBase(ShoesStruct):

    @property
    def auth_data(self):
        return list(bytes(self._auth_data))

    @auth_data.setter
    def auth_data(self, auth_data):
        self.num_auth = len(auth_data)
        self._auth_data = (self._auth_data._type_ * len(auth_data))()
        al = bytes(auth_data)
        assert(len(al) == len(auth_data))
        memmove(self._auth_data, al, len(auth_data))

    @classmethod
    def from_bytes(cls, buf):
        try:
            def handle_auth_data_callback(self, buf_without_checksum, initial_len):
                if len(buf_without_checksum) != initial_len:
                    self.auth_data = buf_without_checksum[initial_len:]
                return self

            self = super().from_bytes(buf, handle_auth_data_callback)
            return self
        except Exception:
            raise

    def to_bytes(self, include_checksum = True):
        res = super().to_bytes(include_checksum = False) + memoryview(self._auth_data)
        if include_checksum:
            res += self.calculate_checksum(res)
        return res

class ServerChoice(ShoesAuthBase):
    _fields_ = [('version', c_uint8),
                ('chosen_auth', c_uint8)]
    _auth_data = (c_ubyte * 0)()

    def __init__(self, version = None, chosen_auth = None, auth_data = None):
        super().__init__()
        if version is not None:
            self.version = version
        if chosen_auth is not None:
            self.chosen_auth = chosen_auth
        if auth_data is not None:
            self.auth_data = auth_data



class ClientAuth(ShoesAuthBase):
    _fields_ = [('version', c_uint8)]
    _auth_data = (c_ubyte * 0)()

    def __init__(self, version = None, auth_data = None):
        super().__init__()
        if version is not None:
            self.version = version
        if auth_data is not None:
            self.auth_data = auth_data


class ClientConnectionRequest(ShoesStruct):
    _fields_ = [('version', c_uint8),
                ('command', c_uint8),
                ('reserved', c_uint8),
                ('address_type', c_uint8),
                ('address', c_uint32),
                ('port', c_uint16)]
    
    def __init__(self, version = None, command = None, address = None, port = None):
        super().__init__()
        if version is not None:
            self.version = version
        if command is not None:
            self.command = command
        if address is not None:
            self.address = address
            self.address_type = SHOES_ADDRESS_TYPE_IPV4
        if port is not None:
            self.port = port
        self.reserved = 0
        
class ServerConnectionResponse(ShoesStruct):
    _fields_ = [('version', c_uint8),
                ('status', c_uint8),
                ('reserved', c_uint8),
                ('address_type', c_uint8),
                ('address', c_uint32),
                ('port', c_uint16)]
    
    def __init__(self, version = None, status = None, address = None, port = None):
        super().__init__()
        if version is not None:
            self.version = version
        if status is not None:
            self.status = status
        if address is not None:
            self.address = address
            self.address_type = SHOES_ADDRESS_TYPE_IPV4
        if port is not None:
            self.port = port
        self.reserved = 0
    
# Resources for implementing variable-length ctypes structures:
#  https://wumb0.in/a-better-way-to-work-with-raw-data-types-in-python.html
#  https://stackoverflow.com/questions/7015487/ctypes-variable-length-structures
#  http://dabeaz.blogspot.com/2009/08/python-binary-io-handling.html
#  https://stackoverflow.com/questions/8392203/dynamic-arrays-and-structures-in-structures-in-python
#  https://docs.python.org/2.5/lib/ctypes-variable-sized-data-types.html

def test():
    cg1 = ClientGreeting()
    cg1.version = SHOES_PROTOCOL_VERSION
    cg1.auth_list = [SHOES_AUTH_TYPE_XOR]
    assert(cg1.to_bytes().hex() == "5a01fedd749c2e")

    cg2 = ClientGreeting.from_bytes(cg1.to_bytes())
    assert(cg2.version == SHOES_PROTOCOL_VERSION)
    assert(cg2.num_auth == 1)
    assert(cg2.auth_list == [SHOES_AUTH_TYPE_XOR])

    cg3 = ClientGreeting(version = SHOES_PROTOCOL_VERSION, auth_list = [SHOES_AUTH_TYPE_XOR])
    assert(cg3.to_bytes().hex() == cg1.to_bytes().hex())

    sc1 = ServerChoice.from_bytes(bytes.fromhex("5afe2c91605e14c8b11b"))
    assert(bytes(sc1.auth_data).hex() == "2c91605e")

    ca1 = ClientAuth(version = SHOES_PROTOCOL_VERSION, auth_data = b'\x2c\xd2\x33\x1f')
    assert(ca1.to_bytes().hex() == "5a2cd2331fa90bb96a")

    ccr1 = ClientConnectionRequest.from_bytes(bytes.fromhex("5a010001c0a8ad0a005074f2be19"))
    assert(ccr1.version == SHOES_PROTOCOL_VERSION)
    assert(ccr1.command == SHOES_COMMAND_ESTABLISH_TCP_IP)
    assert(ccr1.reserved == 0)
    assert(ccr1.address_type == SHOES_ADDRESS_TYPE_IPV4)
    assert(str(ipaddress.IPv4Address(ccr1.address)) == "192.168.173.10")
    assert(ccr1.port == 80)

    ccr2 = ClientConnectionRequest(version = SHOES_PROTOCOL_VERSION, command = SHOES_COMMAND_ESTABLISH_TCP_IP,
                                         address = int(ipaddress.IPv4Address("192.168.173.10")), port = 80)
    assert(ccr2.to_bytes().hex() == "5a010001c0a8ad0a005074f2be19")

    scr1 = ServerConnectionResponse.from_bytes(bytes.fromhex("5a000001000000000000ebcb7543"))
    assert(scr1.version == SHOES_PROTOCOL_VERSION)
    assert(scr1.status == SHOES_STATUS_SUCCESS)
    assert(scr1.reserved == 0)
    assert(scr1.address_type == SHOES_ADDRESS_TYPE_IPV4)
    assert(str(ipaddress.IPv4Address(scr1.address)) == "0.0.0.0")
    assert(scr1.port == 0)

if __name__ == "__main__":
    test()