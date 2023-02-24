import socket
from concurrent import futures
from collections import defaultdict
import grpc

import chatapp_pb2, chatapp_pb2_grpc

users = defaultdict(list)


def get_pending_messages(username: str) -> "list[str]":
    if not (username in users):
        return []
    return users[username]


def clear_pending_messages(username: str) -> None:
    if username in users:
        users[username] = []


def return_pending_messages(username: str) -> "list[str]":
    if username in users:
        messages = get_pending_messages(username)
        clear_pending_messages(username)
        return messages
    return []


def delete_user(username: str) -> None:
    if username in users:
        del users[username]
        return True
    return False


def command_join(username):
    return (
        "User created successfully. Welcome!"
        if not users.setdefault(username, [])
        else "Welcome back!"
    )


def command_list(wildcard: str = "") -> str:
    return ", ".join([k for k in users.keys() if wildcard in k])


def command_delete(username):
    print("Handling delete action")
    result = delete_user(username)
    return "User deleted successfully." if result else "User does not exist."


def send(sender, receiver, message):
    message = f"{sender} says: {message}"
    if receiver not in users:
        return f"The recipient '{receiver}' does not exist."
    users[receiver].append(message)
    return "Message sent successfully."


class Chat(chatapp_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        pass
        self.actions = {
            "list": command_list,
            "delete": command_delete,
            "join": command_join,
            "logout": lambda username: "",
        }

    def Listen(self, request, context):
        pending_messages = return_pending_messages(request.username)
        return chatapp_pb2.PendingRes(
            message="\n".join(pending_messages), isEmpty=len(pending_messages) == 0
        )

    def Packet(self, request, context):
        action = request.action
        username = request.username
        print("Handling action:", action, "for user:", username)
        func = self.actions.get(action, lambda username: "Invalid action")
        return chatapp_pb2.User(text=func(username))

    def Chat(self, request, context):
        if request.sender and request.receiver and request.text:
            message = send(request.sender, request.receiver, request.text)
            return chatapp_pb2.User(text=message)


def main(
    host: str = socket.gethostbyname(socket.gethostname()), port: int = 3000
) -> None:

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
