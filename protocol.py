import struct
from codes import Requests, Responses

# Big Endian Format
# b = Version of our wire protocol (byte)
# l = Size of our message (long)
# b = Operation (byte)

HEADER_FORMAT = ">blb"
HEADER_SIZE = 1 + 4 + 1
MAX_SIZE = 2<<32 - 1
VERSION=1
ENCODING = 'utf-8'

class WireProtocol:
    @staticmethod
    def get_header(version, size, operation):
        return struct.pack(HEADER_FORMAT, version, size, operation)
    
    @staticmethod
    def encode(version, operation, msg: str):
        encoded = msg.encode(ENCODING)
        msg_size = len(encoded)
        header = WireProtocol.get_header(version, msg_size, operation)
        return header, encoded
    

    @staticmethod
    def decode_header(header):
        version, size, operation = struct.unpack(HEADER_FORMAT, header)
        return version, size, operation
        

