import grpc
import chat_pb2
import chat_pb2_grpc

class ChatClient:
    def __init__(self, host="localhost", port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = chat_pb2_grpc.ChatServiceStub(self.channel)

    def login(self, username):
        request = chat_pb2.User(username=username)
        response = self.stub.Login(request)
        return response.success, response.message

    def create_account(self, username):
        request = chat_pb2.User(username=username)
        response = self.stub.CreateAccount(request)
        return response.success, response.message

    def delete_account(self, username):
        request = chat_pb2.User(username=username)
        response = self.stub.DeleteAccount(request)
        return response.success, response.message

    def list_accounts(self, pattern):
        request = chat_pb2.ListAccountsRequest(pattern=pattern)
        response = self.stub.ListAccounts(request)
        return response.usernames

    def send_message(self, sender, receiver, text):
        request = chat_pb2.Message(sender=sender, receiver=receiver, text=text)
        response = self.stub.SendMessage(request)
        return response.success, response.message
