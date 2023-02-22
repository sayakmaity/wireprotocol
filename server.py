import socket
import threading
import sys
from concurrent import futures

import grpc

import chatapp_pb2, chatapp_pb2_grpc

users_connections = {}
users = {}
# Event that is set when threads are running and cleared when you want threads to stop
run_event = threading.Event()

def create_user(username: str) -> bool:
    if (username in users):
        return False
    users[username] = []
    return True

def list_users(wildcard: str) -> "list[str]":

    temp = list(users.keys())
    if wildcard:
        temp = list(filter(lambda x: wildcard in x, temp))

    return temp

def add_pending_message(username: str, message: str) -> bool:

    create_user(username)
    users[username].append(message)


def get_pending_messages(username: str) -> "list[str]":

    if not (username in users):
        return []
    return users[username]


def clear_pending_messages(username: str) -> None:

    if (username in users):
        users[username] = []


def return_pending_messages(username: str) -> "list[str]":

    if (username in users):
        messages = get_pending_messages(username)
        clear_pending_messages(username)
        return messages
    return []


def delete_user(username: str) -> None:
    if (username in users):
        del users[username]
    return

def handle_payload(payload: "list[str]"):

    print("Handling payload:", payload)

    payload = payload[1:]
    if payload[0] == "join":
        success = create_user(payload[1])
        return (
            success,
            "User created successfully. Welcome!" if success else "Welcome back!",
        )
    elif payload[0] == "list":
        print("Handling list action")
        if len(payload) == 1:
            payload.append("")
        users = list_users(payload[1])
        print("Retrieved users: ", users)
        return (users, ", ".join(users))
    elif payload[0] == "delete":
        print("Handling delete action")
        result = delete_user(payload[1])
        print("Deletion result: ", result)
        return (
            result,
            "User deleted successfully." if result else "User does not exist.",
        )
    else:
        return (None, None)


def handle_send_grpc(sender, receiver, message):
    message = f"{sender} says: {message}"
    if receiver in users:
        add_pending_message(receiver, message)
        return "Message sent successfully."
    else:
        return "The receipient does not exist."


# gRPC implementation
class Chat(chatapp_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        pass

    # client <> client communication
    def ListenToPendingMessages(self, request, context):
        pending_messages = return_pending_messages(request.username)
        return chatapp_pb2.PendingMsgsResponse(
            message="\n".join(pending_messages), isEmpty=len(pending_messages) == 0
        )

    def Packet(self, request, context):
        action = request.action
        username = request.username

        if action == "list":
            payload = [None, action, username]
            return chatapp_pb2.User(text=handle_payload(payload)[1])

        elif action == "delete":
            if username in users_connections.keys():
                return chatapp_pb2.User(text="Cannot delete logged in user.")

            payload = [None, action, username]
            return chatapp_pb2.User(text=handle_payload(payload)[1])

        elif action == "join":
            if username in users_connections.keys():  # already logged in, refuse client
                return chatapp_pb2.User(text="Already logged in elsewhere.")

            users_connections[username] = None
            return chatapp_pb2.User(text=handle_payload([None, "join", username])[1])

        elif action == "quit":
            if username in users_connections.keys():
                del users_connections[username]
            return chatapp_pb2.User(text="")
        else:
            return chatapp_pb2.User(text="Invalid action")

    def Chat(self, request, context):
        if request.sender and request.receiver and request.text:
            message = handle_send_grpc(request.sender, request.receiver, request.text)
            return chatapp_pb2.User(text=message)


def main(host: str = "127.0.0.1", port: int = 3000) -> None:
    """
    Initializes the server.
    @Parameter: None.
    @Returns: None.
    """
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        chatapp_pb2_grpc.add_ChatServiceServicer_to_server(Chat(), server)
        server.add_insecure_port(f"{host}:{port}")
        server.start()
        print(f"Now listening on {host}:{port}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop
        print("Server stopped.")


if __name__ == "__main__":
    main()
