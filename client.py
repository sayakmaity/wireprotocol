import socket
import logging
from codes import Requests, Responses

class Client:
    """
    A class representing a client that can send messages to the server.

    Parameters:
    host (str): The IP address of the server to connect to.
    port (int): The port number to use for the server.
    header_length (int, optional): The header size of the message in bytes. Defaults to 64.
    encoding (str, optional): The encoding format to use for the messages. Defaults to 'utf-8'.
    """
    def __init__(self, host, port=5050, header_length=64, encoding='utf-8'):
        self.host = host
        self.port = port
        self.header_length = header_length
        self.encoding = encoding
        self.addr = (host, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.addr)

    def start_logger(self):
        """
        Start the logger for the client.
        """
        logging.basicConfig(level=logging.INFO,
        handlers=[
                logging.FileHandler("client_debug.log"),
                logging.StreamHandler()
            ]
        )

    def send_message(self, msg):
        """
        Send a message to the connected server.

        Parameters:
        msg (str): The message to send.
        """
        try:
            message = msg.encode(self.encoding)
            msg_len = len(message)
            send_length = str(msg_len).encode(self.encoding)
            send_length += b' ' * (self.header_length - len(send_length))
            self.client.send(send_length)
            self.client.send(message)
            return self.client.recv(2048).decode(self.encoding)
        except Exception as e:
            logging.exception(e)
            return None

    def disconnect(self):
        """
        Disconnect from the server.
        """
        self.send_message(Requests.DISCONNECT)
        self.client.close()

    def create_account(self, username: str):
        try:
            response = self.send_message(f"{Requests.CREATE_ACCOUNT}{username}")
            status = response[:2]
            message = response[2:]
            if status == Responses.SUCCESS:
                logging.info(f"[ACCOUNT CREATION] Account created successfully for username: {username}")
                return True
            else:
                logging.warning(f"[ACCOUNT CREATION] Account creation failed for username: {username}. Reason: {message}")
                return False
        except Exception as e:
            logging.exception(f"[CREATE ACCOUNT] Exception occurred while deleting account {username}: {e}")
            return False

    def delete_account(self, username: str):
        try:
            response = self.send_message(f"{Requests.DELETE_ACCOUNT}{username}")
            status = response[:2]
            message = response[2:]
            if status == Responses.SUCCESS:
                logging.info(f"[DELETE ACCOUNT] Account {username} deleted")
                return True
            else:
                logging.error(f"[DELETE ACCOUNT] Failed to delete account {username}. Reason: {message}")
                return False
        except Exception as e:
            logging.exception(f"[DELETE ACCOUNT] Exception occurred while deleting account {username}: {e}")
            return False

if __name__ == '__main__':
    client = Client('10.250.37.222')
    client.start_logger()
    client.create_account('jchiu')
    client.create_account('cathy')
    client.create_account('jchiu')
    client.delete_account('jchiu')
    client.create_account('jchiu')
    client.disconnect()
