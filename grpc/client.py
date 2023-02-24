import threading
import grpc
import time

import chatapp_pb2, chatapp_pb2_grpc


def get_username() -> str:
    while True:
        username = input().strip()
        if not username:
            continue
        break
    return username


def join_chat(username: str, stub) -> str:
    response = stub.Packet(chatapp_pb2.Request(action="join", username=username))
    return response.text


def listen_to_pending_messages(username: str, stub) -> None:
    try:
        while True:
            time.sleep(1)
            response = stub.Listen(
                chatapp_pb2.Request(username=username)
            )
            if not response.isEmpty:
                print(response.message)
    except:
        print("Closing the application.")


def list_command(username: str, stub, command: list) -> None:
    if len(command) == 1:
        command.append("")
    response = stub.Packet(chatapp_pb2.Request(action=command[0], username=command[1]))
    print(response.text, flush=True)


def send_command(username: str, stub, command: list) -> None:
    if len(command) < 2:
        print(
            "Please specify a valid user to send the message to.",
            flush=True,
        )
        return
    print(f"What message would you like to send to {' '.join(command[1:])}?")

    while True:
        message = input(">>> ")
        if not message:
            continue
        break

    response = stub.Chat(
        chatapp_pb2.Message(
            sender=username,
            receiver=" ".join(command[1:]),
            text=message,
        )
    )


def delete_command(username: str, stub, command: list) -> None:
    if len(command) != 2:
        print(
            "Couldn't find the user - check the spelling and try again.",
            flush=True,
        )
        return
    if username == " ".join(command[1:]):
        print("You cannot delete your own account.", flush=True)
        return
    response = stub.Packet(
        chatapp_pb2.Request(action=command[0], username=" ".join(command[1:]))
    )
    print(response.text, flush=True)


def quit_command(username: str, stub, command: list) -> str:
    response = stub.Packet(chatapp_pb2.Request(action=command[0], username=username))
    return response.text


def main(host="10.250.103.17", port=3000):
    print(f"Connecting to server at {host}:{port}...")
    with grpc.insecure_channel(f"{host}:{port}") as channel:
        stub = chatapp_pb2_grpc.ChatServiceStub(channel)
        print(
            "Type username to login or create acc",
            flush=True,
        )
        username = get_username()
        response = join_chat(username, stub)

        listen_thread = threading.Thread(
            target=listen_to_pending_messages, args=(username, stub)
        )
        listen_thread.start()
        commands = {
            "list": list_command,
            "send": send_command,
            "delete": delete_command,
            "logout": quit_command,
        }
        print(
            "\n\033[1mActions:\033[0m\n\033[32m  list <wildcard, optional>\033[0m\n\033[34m  send <user>\033[0m\n\033[31m  delete <user>\033[0m\n\033[33m  logout\033[0m\n",
            flush=True,
        )
        try:
            while True:
                command = input("enter command >>>").split()
                if not command:
                    continue
                if command[0] in commands:
                    func = commands[command[0]]
                    func(username, stub, command)
                    if command[0] == "logout":
                        return
        except KeyboardInterrupt:
            stub.Chat(chatapp_pb2.Request(action="logout", username=username))
        listen_thread.join()


if __name__ == "__main__":
    main()
