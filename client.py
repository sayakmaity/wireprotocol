import sys
import socket
import threading
import grpc
import time

import chatapp_pb2, chatapp_pb2_grpc

# Event that is set when threads are running and cleared when you want threads to stop
run_event = threading.Event()
# Event to block client UI until server response
respond_event = threading.Event()

def main(host: str = "10.250.103.17", port: int = 3000) -> None:
    print(f"Starting connection to {host}:{port}")

    # listen_thread = None
    with grpc.insecure_channel(f"{host}:{port}") as channel:
        stub = chatapp_pb2_grpc.ChatServiceStub(channel)

        print("Enter username (will be created if it doesn't exist): ", flush=True)
        while True:
            username = input()
            if not username:
                continue
            break

        response = stub.Packet(chatapp_pb2.Request(action="join", username=username))
        print(response.text, flush=True)

        # user logged in elsewhere, end client
        if "Already logged in" in response.text:
            return

        def periodically_listen():
            print("Listening to pending messages...")
            try:
                while True:
                    time.sleep(2)
                    response = stub.ListenToPendingMessages(
                        chatapp_pb2.Request(username=username)
                    )
                    if not response.isEmpty:
                        print(response.message)
            except:
                print("Shutting down.")
            return

        listen_thread = threading.Thread(target=(periodically_listen), args=())
        listen_thread.start()

        # print("Actions: list <wildcard, optional>, send <user>, delete <user>, quit", flush=True)
        print("\n\033[1mActions:\033[0m\n\033[32m  list <wildcard, optional>\033[0m\n\033[34m  send <user>\033[0m\n\033[31m  delete <user>\033[0m\n\033[33m  quit\033[0m\n", flush=True)


        try:
            while True:
                action = input("enter commmand >>>")

                action_list = action.split()

                if len(action_list) == 0:
                    continue

                elif action_list[0] == "list":
                    print(len(action_list))
                    if len(action_list) == 1:
                        action_list.append("")
                    response = stub.Packet(
                        chatapp_pb2.Request(action=action_list[0], username=action_list[1])
                    )
                    print(response.text, flush=True)

                elif action_list[0] == "send":
                    if len(action_list) < 2:
                        print(
                            "Must specify valid user to send to. Try again.",
                            flush=True,
                        )
                        continue
                    print(
                        "Message to send to {user}?".format(
                            user=" ".join(action_list[1:])
                        )
                    )

                    while True:
                        message = input(">>> ")
                        if not message:
                            continue
                        break

                    response = stub.Chat(
                        chatapp_pb2.Message(
                            sender=username,
                            receiver=" ".join(action_list[1:]),
                            text=message,
                        )
                    )

                elif action_list[0] == "delete":
                    if len(action_list) != 2:
                        print(
                            "Must specify valid user to delete. Try again.",
                            flush=True,
                        )
                        continue
                    if username == " ".join(action_list[1:]):
                        print("Cannot delete self user.", flush=True)
                        continue
                    response = stub.Packet(
                        chatapp_pb2.Request(
                            action=action_list[0], username=" ".join(action_list[1:])
                        )
                    )
                    print(response.text, flush=True)
                elif action_list[0] == "quit":
                    response = stub.Packet(chatapp_pb2.Request(action=action_list[0], username=username))
                    print(response.text, flush=True)
                    return
                else:
                    print("Unrecognized action.", flush=True)
                    continue

            print(response.text, flush=True)

        except KeyboardInterrupt:
            # send quit to server
            response = stub.Chat(chatapp_pb2.Request(action="quit", username=username))
        listen_thread.join()
        return


if __name__ == "__main__":
    main()
