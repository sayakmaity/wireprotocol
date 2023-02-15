import socket
import threading
from codes import Requests, Responses
import logging
import fnmatch
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
        username = msg
        with self.users_lock:
            if username in self.usernames:
                if username in self.active_connections:
                    return self.generate_payload(Responses.FAILURE, True, "User already logged in")
                else:
                    self.active_connections[username] = conn
                    return self.generate_payload(Responses.SUCCESS, True, "User logged in")
            else:
                return self.generate_payload(Responses.FAILURE, True, "Username does not exist")

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
        """
        Handle a list accounts request from a client.
        The method returns a list of all usernames that match the provided regex-like query.

        Parameters:
        conn (socket.socket): The client socket connection.
        msg (str): The query to search for.

        Returns:
        dict: The response metadata in the form of a dictionary.
        """
        query = msg.strip()
        matching_accounts = []
        for username in self.usernames:
            if fnmatch.fnmatch(username, query):
                matching_accounts.append(username)
        if matching_accounts:
            response_message = "\n".join(matching_accounts)
            return self.generate_payload(Responses.SUCCESS, True, f"\n{response_message}")
        else:
            return self.generate_payload(Responses.FAILURE, True, "No matching accounts found.")


    def handle_send_message(self, conn, msg):
        sender, receiver, text_message = msg.split("\n")
        sender = sender.strip()
        receiver = receiver.strip()
        text_message = text_message.strip()

        if receiver not in self.usernames:
            return self.generate_payload(Responses.FAILURE, True, "Receiver not found.")

        receiver_conn = None
        with self.clients_lock:
            for username in self.usernames:
                if username == receiver:
                    receiver_conn = self.active_connections.get(username)
                    break

        if receiver_conn:
            msg = f"\n<{sender}>: {text_message}"

            message = msg.encode(self.encoding)
            msg_len = len(message)
            send_length = str(msg_len).encode(self.encoding)
            send_length += b' ' * (self.header_length - len(send_length))
            
            receiver_conn.send(send_length)
            receiver_conn.send(message)
            return self.generate_payload(Responses.SUCCESS, True, "Message sent.")
        else:
            user = (self.username_to_user[receiver])
            user.add_message(f"\n<{sender}>: {text_message}")
            print(user.message_queue)
            return self.generate_payload(Responses.SUCCESS, True, "Message Queued.")


    def handle_view_messages(self, conn, msg=""):
        with self.users_lock:
            username = None
            for u, connection in self.active_connections.items():
                if connection == conn:
                    username = u
            
            if username:
                user = self.username_to_user[username]
                message = ""
                msg = user.get_message()
                while msg:
                    message += (msg)
                    msg = user.get_message()

                # msg_len = len(message)
                # send_length = str(msg_len).encode(self.encoding)
                # send_length += b' ' * (self.header_length - len(send_length))
                
                # conn.send(send_length)
                # conn.send(message)
                return self.generate_payload(Responses.SUCCESS, True, message)
            else:
                return self.generate_payload(Responses.FAILURE, True, "Server thinks user does not exist.")






    def disconnect(self, conn, msg=""):
        with self.clients_lock:
            index = self.clients.index(conn)
            conn.close()
            self.clients.pop(index)

        with self.users_lock:
            print(self.active_connections)
            if conn in self.active_connections.values():
                for k in self.active_connections.copy():
                    if self.active_connections[k] == conn:
                        del self.active_connections[k]
            print(self.active_connections)
        return self.generate_payload(Responses.SUCCESS, False, "Disconnected!")
    

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
