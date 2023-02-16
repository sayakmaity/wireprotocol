from client import Client
import sys
# Function to display menu to the user
def display_menu():
    print("--- Menu ---")
    print("1. Login to an account")
    print("2. List accounts")
    print("3. Create an account")
    print("4. Delete an account")
    print("5. Exit")

def display_login_menu():
     print("--- Menu ---")
     print("1. Send Message")
     print("2. View Messages")
     print("3. List accounts")

# Function to login to an account
def login(client):
    username = input("Enter your username: ")
    return client.login(username)

# Function to list all accounts
def list_accounts(client):
    query = input("Enter query (* queries all): ")
    return client.list_accounts(query)

# Function to create an account
def create_account(client):
    username = input("Enter your username: ")
    return client.create_account(username)

# Function to delete an account
def delete_account(client):
    username = input("Enter username you want to delete: ")
    return client.delete_account(username)

def send_message(client):
    receiver = input("Enter username of recipient: ")
    message = input("Enter message: ")
    return client.send_chat(receiver, message)

def view_messages(client):
    return client.view_messages()

# Main function to run the program
def main():
    try:
        client = Client('10.250.37.222')
        while client.receive_event.is_set():
            try:
                display_menu()
                choice = input("Enter your choice: ")
                if not choice or not choice.isdigit():
                    print("Please enter a valid choice.")
                else:
                    choice = int(choice)
                    print()
                if choice == 1:
                    if login(client):
                        print()
                        while client.receive_event.is_set():
                            display_login_menu()
                            choice = int(input("Enter your choice: "))
                            print()
                            if choice == 1:
                                send_message(client)
                            elif choice == 2:
                                view_messages(client)
                            elif choice == 3:
                                list_accounts(client)
                            else:
                                print("Invalid choice")

                elif choice == 2:
                    list_accounts(client)
                elif choice == 3:
                    create_account(client)
                elif choice == 4:
                    delete_account(client)
                elif choice == 5:
                    break
                else:
                    print("Invalid choice")
                print()
            except KeyboardInterrupt:
                    print("\nClient exiting.")
                    client.stop_listening_for_messages()
                    client.disconnect()
                    sys.exit(0)
            
    except Exception as e:
        print(e)
        client.disconnect()

# Call the main function
if __name__ == "__main__":
    main()