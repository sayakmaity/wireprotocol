# Function to display menu to the user
def display_menu():
    print("--- Menu ---")
    print("1. Login to an account")
    print("2. List accounts")
    print("3. Create an account")
    print("4. Delete an account")
    print("5. Exit")

# Function to login to an account
def login():
    username = input("Enter your username: ")

    if True:
        print("Login successful")
        return True
    else:
        print("Login failed")
        return False

# Function to list all accounts
def list_accounts():
    print("--- Accounts ---")
    for username in []:
        print(username)

# Function to create an account
def create_account():
    username = input("Enter your username: ")

    if username in []:
        print("Username already exists")
    else:
        # create_user
        pass

# Function to delete an account
def delete_account():
    username = input("Enter your username: ")

    if username in []:
        print("Account deleted successfully")
    else:
        print("Username not found")

# Main function to run the program
def main():
    while True:
        display_menu()
        choice = int(input("Enter your choice: "))

        if choice == 1:
            if login():
                # Do something after successful login
                pass
        elif choice == 2:
            list_accounts()
        elif choice == 3:
            create_account()
        elif choice == 4:
            delete_account()
        elif choice == 5:
            break
        else:
            print("Invalid choice")

# Call the main function
if __name__ == "__main__":
    main()