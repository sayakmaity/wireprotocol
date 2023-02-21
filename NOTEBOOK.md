## Project Management

- Get Client and Server running with dummy messages (no wireprotocol/rpc)
- Modify the client/server communication mechanism to use wire protocol
- Duplicate for gRPC

## Client Requests:

- login: Enter username ands end to server. Once verified, background thread starts listening to messages
- create_account: Enter username and send to server, server handles checking for dupes and state management. Does not require user to be logged in
- delete_account: same as above. Does not require user to be logged in
- list_accounts: Query accounts in a grep-like unix manner. Client sends over query string. Does not require user to be logged in
- send_message: Enter a recipient and a message, once verification is done the message is sent immediately if recipient is online or queued if offline
- view_messages: View queued messages while user was offline.

## How to handle background thread that listens to message?

Issue: Intercepts the response from server unrelated to messages. ie: If I'm creating an account it intercepts the response from the server.

Solution: Use a lock, only check for messages while the background thread has the lock and temproarily give the lock to other request functionalities when performing a request.

## Wire Protocol

Packet headers are structured like the following in big-endian format

| Index | Length | Description                |
|-------|--------|----------------------------|
| 0     | 1      | Version of Protocol        |
| 1     | 4      | Message Size               |
| 5     | 1      | Operation ID (what req/res |

Then, once the recipient decodes the header, we send a message corresponding to the message size in the wire protocol
