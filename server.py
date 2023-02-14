import socket
import threading
from codes import Requests, Responses
import logging
from base_server import BaseServer

from user import User

class Server(BaseServer):
    """
    A class representing a server that can handle multiple clients using threads.

    Attributes:
        host (str): The IP address of the server host.
        port (int): The port number to use for the server.
        encoding (str): The encoding format to use for the messages.
        header_length (int): The header size of the message in bytes.
        server (socket.socket): The server socket instance.

    Parameters:
        host (str, optional): The IP address of the server host. Defaults to the local machine's IP address.
        port (int, optional): The port number to use for the server. Defaults to 5050.
        encoding (str, optional): The encoding format to use for the messages. Defaults to 'utf-8'.
        header_length (int, optional): The header size of the message in bytes. Defaults to 64.
    """
    def __init__(self,
        host: str = socket.gethostbyname(socket.gethostname()),
        port: int = 5050,
        encoding: str = 'utf-8',
        header_length: int = 64,
    ):
        super().__init__(host, port, encoding, header_length)
        
        self.clients_lock = threading.Lock()
        self.clients = []

        self.users_lock = threading.Lock()
        self.usernames = []
        self.username_to_user = {}
        self.active_connections = {}
        self.addr_to_username = {}

        self.requests = {
            Requests.LOGIN: self.handle_login,
            Requests.CREATE_ACCOUNT: self.handle_create_account,
            Requests.DELETE_ACCOUNT: self.handle_delete_account,
            Requests.LIST_ACCOUNTS: self.handle_list_accounts,
            Requests.SEND_MESSAGE: self.handle_send_message,
            Requests.VIEW_MESSAGES: self.handle_view_messages,
            Requests.DISCONNECT: self.disconnect
        }

        # Create a new server socket instance and bind it to the specified host and port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

    def handle_login(self, conn, msg):
        # TODO: handle login request
        pass

    def handle_create_account(self, conn, msg):
        username = msg
        with self.users_lock:
            if username in self.usernames:
                return self.generate_payload(Responses.FAILURE, True, "Username already exists")
            else:
                new_user = User(username)
                self.usernames.append(username)
                self.username_to_user[username] = new_user
                return self.generate_payload(Responses.SUCCESS, True, "User Created")


    def handle_delete_account(self, conn, msg):
        username = msg
        with self.users_lock:
            if username in self.usernames:
                user = self.username_to_user[username]
                del user
                self.usernames.remove(username)
                del self.username_to_user[username]
                return self.generate_payload(Responses.SUCCESS, True, "Account deleted successfully")
            else:
                return self.generate_payload(Responses.FAILURE, True, "Account not found")

    def handle_list_accounts(self, conn, msg):
        # TODO: handle list accounts request
        pass

    def handle_send_message(self, conn, msg):
        # TODO: handle send message request
        pass

    def handle_view_messages(self, conn, msg):
        # TODO: handle view messages request
        pass
    

    def start(self):
        """
        Start the server and listen for incoming connections.
        """
        self.start_logger()
        self.server.listen()
        logging.info(f"[LISTENING] Server is listening on port {self.port}")
        try:
            while True:
                conn, addr = self.server.accept()
                with self.clients_lock:
                    self.clients.append(conn)
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
                logging.info(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        except KeyboardInterrupt:
            logging.info("[SHUTTING DOWN] Closing server socket...")
            self.server.close()
            with self.clients_lock:
                for conn in self.clients:
                    self.disconnect(conn)
            logging.info("[SHUTDOWN COMPLETE] Goodbye!")

if __name__ == "__main__":
    server = Server()
    server.start()
