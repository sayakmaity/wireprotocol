import socket
import threading
from codes import Requests, Responses
import logging

class BaseServer:
    """
    A class representing a server that can handle multiple clients using threads.

    Attributes:
        host (str): The IP address of the server host.
        port (int): The port number to use for the server.
        encoding (str): The encoding format to use for the messages.
        header_length (int): The header size of the message in bytes.
        disconnect_message (str): The message used to disconnect a client.
        server (socket.socket): The server socket instance.

    Parameters:
        host (str, optional): The IP address of the server host. Defaults to the local machine's IP address.
        port (int, optional): The port number to use for the server. Defaults to 5050.
        encoding (str, optional): The encoding format to use for the messages. Defaults to 'utf-8'.
        header_length (int, optional): The header size of the message in bytes. Defaults to 64.
        disconnect_message (str, optional): The message used to disconnect a client. Defaults to '!DISCONNECT'.
    """
    def __init__(self,
        host: str = socket.gethostbyname(socket.gethostname()),
        port: int = 5050,
        encoding: str = 'utf-8',
        header_length: int = 64,
    ):
        self.host = host
        self.port = port
        self.encoding = encoding
        self.header_length = header_length
        self.addr = (self.host, self.port)
        
        self.clients_lock = threading.Lock()
        self.clients = []

        self.requests = {
            Requests.DISCONNECT: self.disconnect
        }

        # Create a new server socket instance and bind it to the specified host and port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

    def start_logger(self):
        """
        Start the logger for the server.
        """
        logging.basicConfig(level=logging.INFO,
        handlers=[
                logging.FileHandler("debug.log"),
                logging.StreamHandler()
            ]
        )

    def broadcast(self, message):
        with self.clients_lock:
            for client in self.clients:
                client.send(message)

    def handle_client(self, conn: socket.socket, addr: tuple):
        """
        A function to handle a single client connection.
        The function listens for incoming messages and sends back a response.

        Parameters:
            conn (socket.socket): The client socket connection.
            addr (tuple): The address of the client in the form (host, port).
        """
        logging.info(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            try:
                msg_length = self.receive_message(conn, self.header_length)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = self.receive_message(conn, msg_length)
                    metadata = self.handle_request(conn, msg)

                    logging.info(f"[{addr}] {metadata}")
                    connected = metadata["server_running"]
                    if not connected:
                        break
                    self.send_message(conn, metadata['status'],  metadata["message"])
                    
            except Exception as e:
                logging.exception(e)
                self.disconnect(conn)
                break

    def receive_message(self, conn, length):
        """
        Receive a message of a specified length from a client connection.

        Parameters:
            conn (socket.socket): The client socket connection.
            length (int): The length of the message to receive.

        Returns:
            str: The received message.
        """
        return conn.recv(length).decode(self.encoding)

    def send_message(self, conn, response_code, message):
        """
        Send a message to a client connection.

        Parameters:
            conn (socket.socket): The client socket connection.
            message (str): The message to send.
        """
        conn.send(f"{response_code}{message}".encode(self.encoding))

    def handle_request(self, conn, msg):
        """
        Handle an incoming request from a client.

        Parameters:
            conn (socket.socket): The client socket connection.
            msg (str): The message received from the client.

        Returns:
            dict: The response metadata in the form of a dictionary.
        """
        try:
            request_code = msg[:2]
            handler = self.requests.get(request_code)
            if handler:
                return handler(conn, msg[2:])
            else:
                return self.generate_payload(Responses.FAILURE, True, "Unrecognized Response")
        except Exception as e:
            logging.exception(e)
    
    def disconnect(self, conn, msg=""):
        with self.clients_lock:
            index = self.clients.index(conn)
            conn.close()
            self.clients.pop(index)
        return self.generate_payload(Responses.SUCCESS, False, "Disconnected!")

    def generate_payload(self, status_code, connected, msg):
        return {
            "status": status_code,
            "server_running": connected,
            "message": msg
        }
