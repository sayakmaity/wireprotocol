# wireprotocol

## Wire Protocol Section

- Run this to get your server host
```
python3
import socket
socket.gethostbyname(socket.gethostname())
```
Copy the output of this and set it to be the parameter for instantiating the client in `messenger.py`

- run `python server.py` to start up the server
- run `python client.py` to connect to the server and start client CLI
