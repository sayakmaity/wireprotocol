import struct
from codes import Requests, Responses

# Define the format of the message header using Big Endian format
# '>' specifies Big Endian
# b specifies a byte
# l specifies a long (4 bytes)
HEADER_FORMAT = ">blb"

# Define the sizes of each component of the message header
# Header is composed of:
# 1 byte version
# 4 bytes message size
# 1 byte operation
HEADER_SIZE = 1 + 4 + 1

# Define the maximum message size
MAX_SIZE = 2<<32 - 1

# Define the current protocol version
VERSION = 1

# Define the message encoding to be used
ENCODING = 'utf-8'

class WireProtocol:
    @staticmethod
    def get_header(version, size, operation):
        """
        Returns the message header as a bytes object, constructed using the specified version, size, and operation.

        Parameters:
        version (int): The version number to use.
        size (int): The size of the message body.
        operation (int): The operation code.

        Returns:
        bytes: The message header.
        """
        return struct.pack(HEADER_FORMAT, version, size, operation)

    @staticmethod
    def encode(version, operation, msg: str):
        """
        Encodes a message as a bytes object, along with its header.

        Parameters:
        version (int): The version number to use.
        operation (int): The operation code.
        msg (str): The message to encode.

        Returns:
        tuple: A tuple containing the message header and the encoded message body as bytes.
        """
        encoded = msg.encode(ENCODING)
        msg_size = len(encoded)
        header = WireProtocol.get_header(version, msg_size, operation)
        return header, encoded

    @staticmethod
    def decode_header(header):
        """
        Decodes the header of a message.

        Parameters:
        header (bytes): The message header.

        Returns:
        tuple: A tuple containing the version number, size of the message body, and operation code.
        """
        version, size, operation = struct.unpack(HEADER_FORMAT, header)
        return version, size, operation
