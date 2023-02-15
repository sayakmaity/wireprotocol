import socket
import logging
import threading
import time
from user import User
from codes import Requests, Responses

def get_lock_decorator(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        with self.lock:
            self.receive_flag = False
        result = func(*args, **kwargs)
        with self.lock:
            self.receive_flag = True
        return result
    return wrapper


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
        self.lock = threading.Lock()
        self.receive_flag = True # indicates if background thread should be listening
        
        self.client.connect(self.addr)
        self._start_logger()
        self.isLoggedIn = False
        self.username = None

    def _start_logger(self):
        """
        Start the logger for the client.
        """
        logging.basicConfig(level=logging.INFO,
        handlers=[
                logging.FileHandler("client_debug.log"),
                logging.StreamHandler()
            ]
        )

    def _receive_ack(self):
        try:
            message_header = self.client.recv(self.header_length)
            if not len(message_header):
                print("[DISCONNECTED] You have been disconnected from the server.")
                self.client.close()
            if message_header.decode(self.encoding).strip():
                message_length = int(message_header.decode(self.encoding).strip())
                message = self.client.recv(message_length).decode(self.encoding)
                return message
        except Exception as e:
            logging.exception(e)
            self.disconnect()

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
            return self._receive_ack()

            # return self.client.recv(2048).decode(self.encoding)
        except Exception as e:
            logging.exception(e)
            return None

    def disconnect(self):
        """
        Disconnect from the server.
        """
        self.send_message(Requests.DISCONNECT)
        self.client.close()

    @get_lock_decorator
    def login(self, username: str):
        try:
            response = self.send_message(f"{Requests.LOGIN}{username}")
            status = response[:2]
            message = response[2:]
            if status == Responses.SUCCESS:
                self.isLoggedIn = True
                self.username = username
                logging.info(f"[LOGIN] User {username} has successfully logged in")
                client.listen_for_messages()
                return True
            else:
                logging.warning(f"[LOGIN] Login failed for username: {username}. Reason: {message}")
                return False
        except Exception as e:
            logging.exception(f"[LOGIN] Exception occurred while logging in as {username}: {e}")
            return False

    @get_lock_decorator
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
            logging.exception(f"[CREATE ACCOUNT] Exception occurred while creating account {username}: {e}")
            return False

    @get_lock_decorator
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

    @get_lock_decorator
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

    @get_lock_decorator
    def send_chat(self, receiver: str, message: str):
        try:
            if not self.isLoggedIn or not self.username:
                logging.warning(f"[SEND MESSAGE] You must be logged in first.")
                return False
            response = self.send_message(f"{Requests.SEND_MESSAGE}{self.username}\n{receiver}\n{message}")
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
    
    @get_lock_decorator
    def view_messages(self):
        try:
            if not self.isLoggedIn or not self.username:
                logging.warning(f"[SEND MESSAGE] You must be logged in first.")
                return False
            response = self.send_message(Requests.VIEW_MESSAGES)
            status = response[:2]
            message = response[2:]
            if status == Responses.SUCCESS:
                # logging.info(f"[VIEW MESSAGES] Messages Found: {message}")
                print(f"Messages Found: {message}")
                return True
            else:
                logging.warning(f"[VIEW MESSAGES] View messages failed due to {message}")
        except Exception as e:
            logging.exception(f"[VIEW MESSAGES] Exception occurred while viewing messages: {e}")
            return False

    def _receive_message(self):
        try:
            message_header = self.client.recv(self.header_length, socket.MSG_DONTWAIT)
            if not len(message_header):
                print("[DISCONNECTED] You have been disconnected from the server.")
                self.client.close()
                self.disconnect()
            if message_header.decode(self.encoding).strip():
                message_length = int(message_header.decode(self.encoding).strip())
                message = self.client.recv(message_length).decode(self.encoding)
                return message    
        except BlockingIOError as e:
            pass
        except Exception as e:
            logging.exception(e)
            self.disconnect()
    
    def listen_for_messages(self):
        receive_thread = threading.Thread(target=self._receive_message_poll)
        receive_thread.start()
        

    
    def _receive_message_poll(self):
        while True:
            try:
                with self.lock:
                    if self.receive_flag:
                        message = self._receive_message()
                        if message:
                            print(f"[Received Message]{message}")
                time.sleep(1)
            except Exception as e:
                logging.exception(e)
                self.disconnect()
                break


if __name__ == '__main__':
    client = Client('10.250.37.222')
    client.listen_for_messages()
    client.create_account("Sayak2")
    # client.run_command(lambda: client.create_account("sayak"))


    # Log out and close the connection
    # client.disconnect()

