# Computer-Networks
Cool Projects for Computer Networks (COMP332)

DV Algo = Distance Vector Routing Algorithm Implementation
- ```router.py ``` calculates the distance between a router (node) and all other routers in a network (graph). 
- The program will output/print the router's distance vector and constantly update itself until it has determined the shortest distance between every two nodes. 

Local Chat = Chat Room Conversation via TCP Connection
- ```chat_server.py``` creates a local server that will administer the conversation. Records incoming user's port and username, sends incoming messages to all users via multiple sockets, and documents/print entire conversation in window. 
- ```chat_client.py``` creates a client that will connect to server. Receives other user's and sends own messages via client-server socket. 
- Run ```python3 chat_server.py``` first and record server's IP address and port. Then create as many clients as you would like by running ```python3 chat_client <username> <server's IP> <server's port>```. Enjoy :)

# Note
I created a two test scripts in "DV Algo" for you to play around with. 
Before you begin, I would advise that you download iTerm2 (a Terminal Emulator for MacOS) in order to run and create you own scripts easily. 
The download link is: https://www.iterm2.com/index.html.
