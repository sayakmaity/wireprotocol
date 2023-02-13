import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()
        self.clients = []
        self.accounts = {}
        self.messages = {}

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024).decode("utf-8")
                if message:
                    self.process_message(client, message)
            except:
                index = self.clients.index(client)
                client.close()
                self.clients.pop(index)
                username = self.get_username(client)
                if username:
                    self.broadcast(f"{username} left the chat!\n")
                break

    def process_message(self, client, message):
        parts = message.split(" ", 1)
        command = parts[0]
        if command == "CREATE":
            if len(parts) == 2:
                username = parts[1]
                if username not in self.accounts:
                    self.accounts[username] = client
                    self.messages[username] = []
                    client.send("200 OK\n".encode("utf-8"))
                else:
                    client.send("400 BAD REQUEST\n".encode("utf-8"))
            else:
                client.send("400 BAD REQUEST\n".encode("utf-8"))
        elif command == "LIST":
            if len(parts) == 2:
                wildcard = parts[1]
                accounts = [username for username in self.accounts if wildcard in username]
                client.send
