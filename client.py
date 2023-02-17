import socket
import logging
import threading
import time
import sys
from codes import Requests, Responses
from protocol import WireProtocol, VERSION, HEADER_SIZE, ENCODING


def get_lock_decorator(func):
    """
    Decorator that acquires and releases a lock around a function call. This
    prevents multiple threads from accessing a shared resource concurrently.
    """
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
    def __init__(self, host, port=5050, header_length=HEADER_SIZE, encoding=ENCODING):
        """
        Initializes a Client object and connects it to the server.

        Parameters:
        host (str): The IP address of the server to connect to.
        port (int): The port number to use for the connection.
        header_length (int): The length of the message header.
        encoding (str): The character encoding to use for message encoding/decoding.
        """
        self.host = host
        self.port = port
        self.header_length = header_length
        self.encoding = encoding
        self.addr = (host, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock = threading.Lock()
        self.receive_flag = True  # Indicates if background thread should be listening
        try:
            self.client.connect(self.addr)
        except ConnectionRefusedError:
            print("Server is off.")
            sys.exit(0)
        self._start_logger()
        self.isLoggedIn = False
        self.username = None
        self.listen_for_messages()

    def _start_logger(self):
        """
        Starts the logger for the client.
        """
        logging.basicConfig(level=logging.INFO,
                            handlers=[logging.FileHandler("client_debug.log"), ])

    def _receive_ack(self):
        """
        Receives an acknowledgment message from the server.

        Returns:
        operation (int): The operation type of the message.
        message (str): The message content.
        """
        try:
            message_header = self.client.recv(self.header_length)
            if not len(message_header):
                print("[DISCONNECTED] You have been disconnected from the server.")
                self.client.close()
                sys.exit(0)
            else:
                version, size, operation = WireProtocol.decode_header(message_header)
                message = self.client.recv(size).decode(self.encoding)
                return operation, message
        except Exception as e:
            logging.exception(e)
            self.stop_listening_for_messages()
            self.client.close()
            sys.exit(0)

    @get_lock_decorator
    def send_message(self, op, msg):
        """
        Sends a message to the connected server.

        Parameters:
        op (int): The type of operation to be performed.
        msg (str): The message to send.

        Returns:
        operation (int): The operation type of the message.
        message (str): The message content.
        """
        try:
            header, encoded = WireProtocol.encode(version=VERSION, operation=op, msg=msg)
            self.client.send(header)
            time.sleep(0.1)
            self.client.send(encoded)
            return self._receive_ack()
        except (BrokenPipeError, OSError) as e:
            logging.error(f"Failed to send message: {e}")
            self.stop_listening_for_messages()
            self.client.close()
            sys.exit(0)

    def disconnect(self):
        """
        Disconnect from the server.
        """
        self.send_message(op=Requests.DISCONNECT, msg="")
        self.client.close()
        sys.exit(0)

    def login(self, username: str):
        """
        Login to the server using the given username.

        Parameters:
        username (str): The username to use for logging in.

        Returns:
        True if the login was successful, False otherwise.
        """
        try:
            # Send the login request to the server.
            status, message = self.send_message(op=Requests.LOGIN, msg=username)
            if status == Responses.SUCCESS:
                # If the login was successful, set the instance variables and log the success.
                self.isLoggedIn = True
                self.username = username
                logging.info(f"[LOGIN] User {username} has successfully logged in")
                print(f"[LOGIN] User {username} has successfully logged in")
                return True
            else:
                # If the login failed, log the failure and return False.
                logging.warning(f"[LOGIN] Login failed for username: {username}. Reason: {message}")
                print(f"[LOGIN] Login failed for username: {username}. Reason: {message}")
                return False
        except Exception as e:
            # If there was an exception, log the exception and return False.
            logging.exception(f"[LOGIN] Exception occurred while logging in as {username}: {e}")
            print(f"[LOGIN] Exception occurred while logging in as {username}: {e}")
            return False

    def create_account(self, username: str):
        """
        Create a new account on the server.

        Parameters:
        username (str): The username to create the account with.

        Returns:
        True if the account was created successfully, False otherwise.
        """
        try:
            # Send the create account request to the server.
            status, message = self.send_message(Requests.CREATE_ACCOUNT, username)
            if status == Responses.SUCCESS:
                # If the account was created successfully, log the success and return True.
                logging.info(f"[ACCOUNT CREATION] Account created successfully for username: {username}")
                print(f"[ACCOUNT CREATION] Account created successfully for username: {username}")
                return True
            else:
                # If the account creation failed, log the failure and return False.
                logging.warning(f"[ACCOUNT CREATION] Account creation failed for username: {username}. Reason: {message}")
                print(f"[ACCOUNT CREATION] Account creation failed for username: {username}. Reason: {message}")
                return False
        except Exception as e:
                logging.exception(f"[CREATE ACCOUNT] Exception occurred while creating account {username}: {e}")
                print(f"[CREATE ACCOUNT] Exception occurred while creating account {username}: {e}")
                return False

    def delete_account(self, username: str):
        """Sends a request to the server to delete the user account with the given username.
        
        Args:
        username (str): The username of the account to be deleted.

        Returns:
        bool: True if the account is successfully deleted, False otherwise.
        """
        try:
            status, message = self.send_message(Requests.DELETE_ACCOUNT, username)
            if status == Responses.SUCCESS:
                logging.info(f"[DELETE ACCOUNT] Account {username} deleted")
                print(f"[DELETE ACCOUNT] Account {username} deleted")
                return True
            else:
                logging.error(f"[DELETE ACCOUNT] Failed to delete account {username}. Reason: {message}")
                print(f"[DELETE ACCOUNT] Failed to delete account {username}. Reason: {message}")
                return False
        except Exception as e:
            logging.exception(f"[DELETE ACCOUNT] Exception occurred while deleting account {username}: {e}")
            print(f"[DELETE ACCOUNT] Exception occurred while deleting account {username}: {e}")
            return False

    def list_accounts(self, pattern: str):
        """Sends a request to the server to retrieve a list of accounts matching the given pattern.
        
        Args:
        pattern (str): The pattern to search for.

        Returns:
        bool: True if the list of accounts is successfully retrieved, False otherwise.
        """
        try:
            status, message = self.send_message(Requests.LIST_ACCOUNTS, pattern)
            if status == Responses.SUCCESS:
                logging.info(f"[LIST ACCOUNTS] Received list of accounts matching pattern {pattern}: {message}")
                print(f"[LIST ACCOUNTS] Received list of accounts matching pattern {pattern}: {message}")
                return True
            else:
                logging.warning(f"[LIST ACCOUNTS] Failed to retrieve list of accounts matching pattern {pattern}. Reason: {message}")
                print(f"[LIST ACCOUNTS] Failed to retrieve list of accounts matching pattern {pattern}. Reason: {message}")
                return False
        except Exception as e:
            logging.exception(f"[LIST ACCOUNTS] Exception occurred while retrieving list of accounts matching pattern {pattern}: {e}")
            print(f"[LIST ACCOUNTS] Exception occurred while retrieving list of accounts matching pattern {pattern}: {e}")
            return False

    def send_chat(self, receiver: str, message: str):
        """Sends a message to another user on the server.

        Args:
        receiver (str): The username of the user to send the message to.
        message (str): The message to send.

        Returns:
        bool: True if the message is successfully sent, False otherwise.
        """
        try:
            if not self.isLoggedIn or not self.username:
                logging.warning(f"[SEND MESSAGE] You must be logged in first.")
                print(f"[SEND MESSAGE] You must be logged in first.")
                return False
            status, message = self.send_message(Requests.SEND_MESSAGE, f"{self.username}\n{receiver}\n{message}")
            if status == Responses.SUCCESS:
                logging.info(f"[SEND MESSAGE] Message sent to {receiver}")
                print(f"[SEND MESSAGE] Message sent to {receiver}")
                return True
            else:
                logging.warning(f"[SEND MESSAGE] Message sending failed to {receiver}. Reason: {message}")
                print(f"[SEND MESSAGE] Message sending failed to {receiver}. Reason: {message}")
                return False
        except Exception as e:
            logging.exception(f"[SEND MESSAGE] Exception occurred while sending message to {receiver}: {e}")
            print(f"[SEND MESSAGE] Exception occurred while sending message to {receiver}: {e}")
            return False
    
    def view_messages(self):
        try:
            if not self.isLoggedIn or not self.username:
                logging.warning(f"[SEND MESSAGE] You must be logged in first.")
                return False
            status, message = self.send_message(Requests.VIEW_MESSAGES, "")
            if status == Responses.SUCCESS:
                print(f"Messages Found: {message}")
                return True
            else:
                logging.warning(f"[VIEW MESSAGES] View messages failed due to {message}")
                print(f"[VIEW MESSAGES] View messages failed due to {message}")
        except Exception as e:
            logging.exception(f"[VIEW MESSAGES] Exception occurred while viewing messages: {e}")
            print(f"[VIEW MESSAGES] Exception occurred while viewing messages: {e}")
            return False

    def _receive_message(self):
        try:
            message_header = self.client.recv(self.header_length, socket.MSG_DONTWAIT)
            if not len(message_header):
                print("[DISCONNECTED] You have been disconnected from the server.")
                self.stop_listening_for_messages()
                self.client.close()
                sys.exit(0)
            else:
                version, size, operation = WireProtocol.decode_header(message_header)
                message = self.client.recv(size).decode(self.encoding)
                return operation, message
        except BlockingIOError as e:
            pass
        except Exception as e:
            logging.exception(e)
            self.stop_listening_for_messages()
            self.client.close()
            sys.exit(0)
    
    def listen_for_messages(self):
        """
        Set the receive event, indicating that the background thread should be listening for messages.
        """
        self.receive_event = threading.Event()
        self.receive_event.set()
        receive_thread = threading.Thread(target=self._receive_message_poll, args=(self.receive_event,))
        receive_thread.start()

    def stop_listening_for_messages(self):
        """
        Clear the receive event, indicating that the background thread should stop listening for messages.
        """
        self.receive_event.clear()

    def _receive_message_poll(self, event):
        """
        Poll for incoming messages from the server, while the receive event is set.

        Parameters:
        event (threading.Event): The receive event.

        Returns:
        None.
        """
        while event.is_set():
            try:
                with self.lock:
                    if self.receive_flag:
                        message = self._receive_message()
                        if message:
                            status, msg = message
                            if status == Responses.DISCONNECT:
                                logging.info("Received disconnect signal. Stopping message polling and closing connection to server.")
                                print("Server disconnected.")
                                self.stop_listening_for_messages()
                                self.client.close()
                                sys.exit(0)
                            elif status == Responses.SUCCESS:
                                print(f"\r\n\n[RECEIVED MESSAGE]{msg}\n\nEnter command: ", end="")
                            else:
                                logging.warning("[RECEIVED UNKNOWN SIGNAL] Disconnecting")
                                self.stop_listening_for_messages()
                                self.client.close()
                                sys.exit(0)
                time.sleep(1)
            except Exception as e:
                logging.exception(e)
                self.stop_listening_for_messages()
                self.client.close()
                sys.exit(0)
