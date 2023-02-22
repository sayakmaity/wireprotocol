import grpc
import time
import chat_pb2
import chat_pb2_grpc
import concurrent

# Define the chat service class
class ChatService(chat_pb2_grpc.ChatServiceServicer):
    # Define a dictionary to store the list of users and their channels
    users = {}

    def Login(self, request, context):
        # Check if the user is already logged in
        if request.username in self.users:
            return chat_pb2.LoginResponse(success=False, message="User already logged in")

        # Add the user to the list of users and create a new channel for them
        self.users[request.username] = context
        return chat_pb2.LoginResponse(success=True, message="User logged in")

    def Logout(self, request, context):
        # Check if the user is logged in
        if request.username not in self.users:
            return chat_pb2.LoginResponse(success=False, message="User not logged in")

        # Remove the user from the list of users and close their channel
        del self.users[request.username]
        context.cancel()
        return chat_pb2.LoginResponse(success=True, message="User logged out")

    def CreateAccount(self, request, context):
        # Check if the username already exists
        if request.username in self.users:
            return chat_pb2.CreateAccountResponse(success=False, message="Username already taken")

        # Add the user to the list of users and create a new channel for them
        self.users[request.username] = context
        return chat_pb2.CreateAccountResponse(success=True, message="Account created")

    def DeleteAccount(self, request, context):
        # Check if the user is logged in
        if request.username not in self.users:
            return chat_pb2.LoginResponse(success=False, message="User not logged in")

        # Remove the user from the list of users and close their channel
        del self.users[request.username]
        context.cancel()
        return chat_pb2.DeleteAccountResponse(success=True, message="Account deleted")

    def ListAccounts(self, request, context):
        # Create a list of usernames matching the pattern
        usernames = [username for username in self.users.keys() if request.pattern in username]
        return chat_pb2.ListAccountsResponse(usernames=usernames)

    def SendMessage(self, request, context):
        # Check if the sender is logged in
        if request.sender not in self.users:
            return chat_pb2.SendMessageResponse(success=False, message="Sender not logged in")

        # Check if the receiver is logged in
        if request.receiver not in self.users:
            return chat_pb2.SendMessageResponse(success=False, message="Receiver not logged in")

        # Send the message to the receiver
        receiver_context = self.users[request.receiver]
        receiver_context.send_initial_metadata(('sender', request.sender),)
        receiver_context.send_message(request)

        return chat_pb2.SendMessageResponse(success=True, message="Message sent")

# Create a gRPC server and add the chat service to it
server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)

# Start the server
print("Starting server...")
server.add_insecure_port('[::]:50051')
server.start()

# Keep the server running
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
