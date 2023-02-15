import argparse
from chat_client import ChatClient

def login(args):
    client = ChatClient()
    if not args.username:
        while True:
            username = input("Username: ")
            if username:
                break
        args.username = username

    success, message = client.login(args.username)
    if success:
        print(f"Welcome, {args.username}!")
        client_thread = Thread(target=client.run)
        client_thread.daemon = True
        client_thread.start()
        while True:
            command = input("> ")
            if command == "quit":
                break
            elif command.startswith("send "):
                _, receiver, *text = command.split()
                text = " ".join(text)
                success, message = client.send_message(args.username, receiver, text)
                if success:
                    print("Message sent.")
                else:
                    print(f"Message failed to send: {message}")
            elif command.startswith("list "):
                _, pattern = command.split()
                accounts = client.list_accounts(pattern)
                print("Accounts:")
                for account in accounts:
                    print(f"  {account}")
            elif command.startswith("create_account "):
                _, username = command.split()
                success, message = client.create_account(username)
                if success:
                    print(f"Account created: {username}")
                else:
                    print(f"Failed to create account: {message}")
            elif command.startswith("delete_account "):
                _, username = command.split()
                success, message = client.delete_account(username)
                if success:
                    print(f"Account deleted: {username}")
                else:
                    print(f"Failed to delete account: {message}")
            else:
                print("Unknown command.")
        client.stop()
    else:
        print(f"Login failed: {message}")
def main():
    parser = argparse.ArgumentParser(description="gRPC chat client")
    parser.set_defaults(func=login)

    subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands", dest="command")
    
    login_parser = subparsers.add_parser("login", help="Log in to the chat server.")
    login_parser.add_argument("username", type=str, nargs="?", default=None, help="The username to log in as.")
    login_parser.set_defaults(func=login)

    send_parser = subparsers.add_parser("send", help="Send a message to a recipient.")
    send_parser.add_argument("receiver", type=str, help="The recipient of the message.")
    send_parser.add_argument("text", type=str, help="The text of the message.")
    send_parser.set_defaults(func=send)

    list_parser = subparsers.add_parser("list", help="List user accounts.")
    list_parser.add_argument("pattern", type=str, nargs="?", default="", help="A pattern to filter the account list.")
    list_parser.set_defaults(func=list_accounts)

    create_account_parser = subparsers.add_parser("create_account", help="Create a new user account.")
    create_account_parser.add_argument("username", type=str, help="The username to create.")
    create_account_parser.set_defaults(func=create_account)

    delete_account_parser = subparsers.add_parser("delete_account", help="Delete a user account.")
    delete_account_parser.add_argument("username", type=str, help="The username to delete.")
    delete_account_parser.set_defaults(func=delete_account)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()