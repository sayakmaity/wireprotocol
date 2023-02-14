import socket
from codes import Requests, Responses

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

class Client:
    """
    A class representing a client that can send messages to the server.

    Parameters:
    host (str): The IP address of the server to connect to.
    port (int): The port number to use for the server.
    """
    def __init__(self, host, port=5050):
        self.host = host
        self.port = port
        self.addr = (host, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.addr)

    def send_message(self, msg):
        """
        Send a message to the connected server.

        Parameters:
        msg (str): The message to send.
        """
        message = msg.encode(FORMAT)
        msg_len = len(message)
        send_length = str(msg_len).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        return self.client.recv(2048).decode(FORMAT)

    def disconnect(self):
        """
        Disconnect from the server.
        """
        self.send_message(DISCONNECT_MESSAGE)
        self.client.close()

    def create_account(self, username: str):
        status = self.send_message(f"{Requests.CREATE_ACCOUNT}{username}")
        print(status)

if __name__ == '__main__':
    client = Client('10.250.37.222')
    client.send_message('Hello World')
    client.send_message('Hello Everyone!')
    client.disconnect()
