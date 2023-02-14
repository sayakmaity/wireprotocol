import socket
import threading

from user import User

class Server:
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
        disconnect_message: str = '!DISCONNECT'
    ):
        self.host = host
        self.port = port
        self.encoding = encoding
        self.header_length = header_length
        self.disconnect_message = disconnect_message
        self.addr = (self.host, self.port)
        
        self.clients_lock = threading.Lock()
        self.clients = []

        self.users_lock = threading.Lock()
        self.usernames = []
        self.username_to_user = {}
        self.active_connections = {}
        self.addr_to_username = {}

        # Create a new server socket instance and bind it to the specified host and port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

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
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            try:
                msg_length = conn.recv(self.header_length).decode(self.encoding)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(self.encoding)
                    request = msg[:2]

                    print(f"[{addr}] {msg}")
                    conn.send("Msg received".encode(self.encoding))

                    if msg == self.disconnect_message:
                        self.close_client(conn)
                        break
                    
            except:
                self.close_client(conn)
                break
    

    def start(self):
        """
        Start the server and listen for incoming connections.
        """
        self.server.listen()
        print(f"[LISTENING] Server is listening on port {self.port}")
        try:
            while True:
                conn, addr = self.server.accept()
                with self.clients_lock:
                    self.clients.append(conn)
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        except KeyboardInterrupt:
            print("[SHUTTING DOWN] Closing server socket...")
            self.server.close()
            with self.clients_lock:
                for conn in self.clients:
                    self.close_client(conn)
            print("[SHUTDOWN COMPLETE] Goodbye!")
    
    def close_client(self, conn):
        with self.clients_lock:
            index = self.clients.index(conn)
            conn.close()
            self.clients.pop(index)
        # username = self.get_username(conn)
        # if username:
        #     self.broadcast(f"{username} left the chat!\n")

if __name__ == "__main__":
    server = Server()
    server.start()
