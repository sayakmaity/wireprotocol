import grpc
import threading
import chat_pb2
import chat_pb2_grpc

# Define the chat client class
class ChatClient:
    def __init__(self):
        # Connect to the chat server
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = chat_pb2_grpc.ChatServiceStub(self.channel)

        # Start a thread to receive messages asynchronously
        self.thread = threading.Thread(target=self.receive_messages)
        self.thread.daemon = True
        self.thread.start()

    def receive_messages(self):
        # Continuously receive messages from the server
        response_iterator = self.stub.SendMessage(chat_pb2.Message(sender='', receiver='', text=''), timeout=None)
        for message in response_iterator:
            if hasattr(message, 'sender'):
                print(f"{message.sender}: {message.text}")


    def login(self, username):
        # Call the Login RPC and return the response
        return self.stub.Login(chat_pb2.User(username=username))

    def logout(self, username):
        # Call the Logout RPC and return the response
        return self.stub.Logout(chat_pb2.User(username=username))

    def create_account(self, username):
        # Call the CreateAccount RPC and return the response
        return self.stub.CreateAccount(chat_pb2.User(username=username))

    def delete_account(self, username):
        # Call the DeleteAccount RPC and return the response
        return self.stub.DeleteAccount(chat_pb2.User(username=username))

    def list_accounts(self, pattern):
        # Call the ListAccounts RPC and print the response
        response = self.stub.ListAccounts(chat_pb2.ListAccountsRequest(pattern=pattern))
        print("Users:")
        for username in response.usernames:
            print(f"- {username}")

    def send_message(self, sender, receiver, text):
        # Call the SendMessage RPC and return the response
        return self.stub.SendMessage(chat_pb2.Message(sender=sender, receiver=receiver, text=text))

# Create a chat client
client = ChatClient()

# Loop to receive commands from the user
while True:
    # Receive a command from the user
    command = input("Enter a command (login/logout/create/delete/list/send/quit): ")

    # Parse the command
    if command == "login":
        username = input("Enter your username: ")
        response = client.login(username)
        if response.success:
            print("Logged in")
        else:
            print(f"Login failed: {response.message}")
    elif command == "logout":
        username = input("Enter your username: ")
        response = client.logout(username)
        if response.success:
            print("Logged out")
        else:
            print(f"Logout failed: {response.message}")
    elif command == "create":
        username = input("Enter a new username: ")
        response = client.create_account(username)
        if response.success:
            print("Account created")
        else:
            print(f"Account creation failed: {response.message}")
    elif command == "delete":
        username = input("Enter the username to delete: ")
        response = client.delete_account(username)
        if response.success:
            print("Account deleted")
        else:
            print(f"Account deletion failed: {response.message}")
    elif command == "list":
        pattern = input("Enter a username pattern: ")
        client.list_accounts(pattern)
    elif command == "send":
        sender = input("Enter your username: ")
        receiver = input("Enter the receiver's username: ")
        text = input("Enter the message: ")
        response = client.send_message(sender, receiver, text)
        if response.success:
            print("Message sent")
        else:
            print(f"Message sending failed: {response.message}")
    elif command == "quit":
        break
    else:
        print("Invalid command")
