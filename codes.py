# A class defining request codes for client-server communication.
class Requests:
    # Integer codes representing different client requests.
    LOGIN = 0
    CREATE_ACCOUNT = 1
    DELETE_ACCOUNT = 2
    LIST_ACCOUNTS = 3
    SEND_MESSAGE = 4
    VIEW_MESSAGES = 5
    DISCONNECT = 6

# A class defining response codes for client-server communication.
class Responses:
    # Integer codes representing different server responses.
    SUCCESS = 7
    FAILURE = 8
    DISCONNECT = 9
    PROTOCOL_ERR = 10
