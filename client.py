import socket
import logging
import threading
import asyncio
import signal
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

    def login(self, username: str):
        try:
            response = self.send_message(f"{Requests.LOGIN}{username}")
            status = response[:2]
            message = response[2:]
            if status == Responses.SUCCESS:
                logging.info(f"[LOGIN] User {username} has successfully logged in")
                return True
            else:
                logging.warning(f"[LOGIN] Login failed for username: {username}. Reason: {message}")
                return False
        except Exception as e:
            logging.exception(f"[LOGIN] Exception occurred while logging in as {username}: {e}")
            return False


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

    def list_accounts(self, pattern: str):
        try:
            response = self.send_message(f"{Requests.LIST_ACCOUNTS}{pattern}")
            status = response[:2]
            message = response[2:]
            if status == Responses.SUCCESS:
                logging.info(f"[LIST ACCOUNTS] Received list of accounts matching pattern {pattern}: {message}")
                return True
            else:
                logging.warning(f"[LIST ACCOUNTS] Failed to retrieve list of accounts matching pattern {pattern}. Reason: {message}")
                return False
        except Exception as e:
            logging.exception(f"[LIST ACCOUNTS] Exception occurred while retrieving list of accounts matching pattern {pattern}: {e}")
            return False

    def send_chat(self, sender: str, receiver: str, message: str):
        try:
            response = self.send_message(f"{Requests.SEND_MESSAGE}{sender}\n{receiver}\n{message}")
            status = response[:2]
            message = response[2:]
            if status == Responses.SUCCESS:
                logging.info(f"[SEND MESSAGE] Message sent to {receiver}")
                return True
            else:
                logging.warning(f"[SEND MESSAGE] Message sending failed to {receiver}. Reason: {message}")
                return False
        except Exception as e:
            logging.exception(f"[SEND MESSAGE] Exception occurred while sending message to {receiver}: {e}")
            return False


    def receive_message(self):
        while True:
            try:
                message_header = self.client.recv(self.header_length)
                if not len(message_header):
                    print("[DISCONNECTED] You have been disconnected from the server.")
                    self.client.close()
                    break

                message_length = int(message_header.decode(self.encoding).strip())
                message = self.client.recv(message_length).decode(self.encoding)

                print(f"[RECEIVED MESSAGE] {message}")
            except Exception as e:
                logging.exception(e)
                self.disconnect()
                break

    def start(self):
        self.client.connect(self.addr)

    
    def main(self):
        try:
            receive_thread = threading.Thread(target=self.receive_message)
            receive_thread.start()
            signal.pause()
        except (KeyboardInterrupt, SystemExit):
            logging.info("Shutting down client")
            self.disconnect()


if __name__ == '__main__':
    client = Client('10.250.37.222')
    client.start()
    client.start_logger()
    client.create_account("sayak") # replace "johndoe" with the desired username

    # Start the async message receiver
    client.login("sayak")
    client.main()

    # Log out and close the connection
    # client.disconnect()

