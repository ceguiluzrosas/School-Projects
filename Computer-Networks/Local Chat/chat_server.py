import datetime
import threading
import socket
import sys

class ChatProxy():

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.server_backlog = 1
        self.chat_list = {}
        self.chat_id = 0
        self.lock = threading.Lock()
        self.start()

    def start(self):
        '''Initialize server socket on which to listen for connections'''
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.bind((self.server_host, self.server_port))
            self.server_port = server_sock.getsockname()[1]
            print ("Server IP: "+str(self.server_host))
            print ("Server Port: "+str(self.server_port))
            server_sock.listen(self.server_backlog)
        except OSError as e:
            print ("Unable to open server socket")
            if server_sock:
                server_sock.close()
            sys.exit(1)

        # Wait for user connection
        while True:
            conn, addr = server_sock.accept()
            self.add_user(conn, addr)
            thread = threading.Thread(target = self.serve_user, args = (conn, addr, self.chat_id))
            thread.start()

    def add_user(self, conn, addr):
        '''Adds a new user to chat and store's information in dic'''
        print ('User has connected:', addr[1])
        self.chat_id = self.chat_id + 1
        self.lock.acquire()
        self.chat_list[self.chat_id] = (conn, addr)
        self.lock.release()

    def read_data(self, conn):
        '''
        Server constantly receives and reads messages from clients in the chat via
        multiple client-server sockets.
        '''
        while True:
            msg = conn.recv(1028).decode('utf-8').split("\r\n")
            name = msg[0]
            byte_length = int(msg[1][8:])
            if byte_length == 0: # Goodbye Message
                return [-1,name]
            else:
                data = [1, name+": "+msg[2]]
                print (data[1]) #print (Name: Message) in terminal window
                return data


    def serve_user(self, conn, addr, client):
        '''
        If client has left chat, this function will call on its removal
        If client has not left chat, then the function will call on send data
        '''
        while True:
            data = self.read_data(conn)
            # data = [-1 or 1, either name of client or text data]
            if data[0] == -1:
                goodbye = "{} has left the chat.".format(data[1])
                print (goodbye)
                self.send_data(client, goodbye)
                self.cleanup(conn)
                break
            self.send_data(client, data[1])


    def send_data(self, client, data):
        '''
        Function will send the message the server has read to every client except
        the original sender
        '''
        self.lock.acquire()
        bin_message = data.encode('utf-8')
        for iD in self.chat_list:
            if client != iD:
                self.chat_list[iD][0].sendall(bin_message)
        self.lock.release()


    def cleanup(self, conn):
        '''
        If the client has decided to leave the chat (by pressing ENTER once), then
        this function will remove the client from dictionary based on connection number.
        '''
        self.lock.acquire()
        for ids in self.chat_list:
            if self.chat_list[ids][0] == conn:
                del self.chat_list[ids]
                break
        self.lock.release()

def main():
    
    print (sys.argv, len(sys.argv))
    server_host = socket.gethostbyname(socket.gethostname())
    server_port = 0
    # Using Port 0 triggers the OS to search for and allocate
    # the next available port.
    chat_server = ChatProxy(server_host, server_port)


if __name__ == '__main__':
    main()
