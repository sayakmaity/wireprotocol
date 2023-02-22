import socket
import threading
from codes import Requests, Responses
from protocol import WireProtocol, VERSION, HEADER_SIZE, ENCODING
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
        encoding: str = ENCODING,
        header_length: int = HEADER_SIZE,
    ):
        self.host = host
        self.port = port
        self.encoding = encoding
        self.header_length = header_length
        self.addr = (self.host, self.port)
        
        self.clients_lock = threading.Lock()
        self.clients = []

        self.requests = {}

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
                header = self.receive_message(conn, self.header_length)
                if header:
                    version, msg_length, operation = WireProtocol.decode_header(header)
                    msg = self.receive_message(conn, msg_length).decode(self.encoding)
                    metadata = self.handle_request(conn, operation, msg)

                    logging.info(f"[{addr}] {metadata}")
                    connected = metadata["server_running"]
                    if not connected:
                        break
                    self.send_message(conn, metadata['status'],  metadata["message"])
            except (OSError, BrokenPipeError, ConnectionResetError):
                # This means the client has disconnected
                logging.error(f"[DISCONNECT] {addr} disconnected unexpectedly")
                break
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
        return conn.recv(length)

    def send_message(self, conn, response_code, message):
        """
        Send a message to a client connection.

        Parameters:
            conn (socket.socket): The client socket connection.
            message (str): The message to send.
        """
        header, encoded = WireProtocol.encode(version=1, operation=response_code, msg=message)
        conn.send(header)
        conn.send(encoded)

    def handle_request(self, conn, op, msg):
        """
        Handle an incoming request from a client.

        Parameters:
            conn (socket.socket): The client socket connection.
            msg (str): The message received from the client.

        Returns:
            dict: The response metadata in the form of a dictionary.
        """
        try:
            handler = self.requests.get(op)
            if handler:
                return handler(conn, msg)
            else:
                return self.generate_payload(Responses.FAILURE, True, "Unrecognized Response")
        except Exception as e:
            logging.exception(e)
    
    def disconnect(self, conn, msg=""):
        """
        Handle a disconnect request from a client.

        Parameters:
        conn (socket.socket): The client socket connection.
        msg (str, optional): The request message. Defaults to an empty string.

        Returns:
        dict: The response metadata in the form of a dictionary.
        """
        with self.clients_lock:
            index = self.clients.index(conn)
            conn.close()
            self.clients.pop(index)
        return self.generate_payload(Responses.SUCCESS, False, "Disconnected!")

    def generate_payload(self, status_code, connected, msg):
        """
        Generate a dictionary containing the response metadata.

        Parameters:
        status_code (int): The response status code.
        connected (bool): Whether the server is still running or not.
        msg (str): The message to include in the response.

        Returns:
        dict: A dictionary containing the response metadata.
        """
        return {
            "status": status_code,
            "server_running": connected,
            "message": msg
        }
