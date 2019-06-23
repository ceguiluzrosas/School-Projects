import threading
import socket
import sys


class ChatClient:

    def __init__(self, chat_host, chat_port, client_name):
        self.chat_host = chat_host
        self.chat_port = chat_port
        self.client_name = client_name
        self.start()


    def start(self):
        '''Opens TCP connection to chat'''
        try:
            chat_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            chat_sock.connect((self.chat_host, self.chat_port))
            print("Connected to socket")
        except OSError as e:
            print("Unable to connect to socket: ")
            if chat_sock:
                chat_sock.close()
            sys.exit(1)

        # One thread for writing and another thread for reading
        threading.Thread(target=self.write_sock, args=(chat_sock,)).start()
        threading.Thread(target=self.read_sock, args=(chat_sock,)).start()

    def send_msg(self, sock, byte_len, txt):
        message = self.client_name + "\r\n" + byte_len + "\r\n" + txt + "\r\n"
        sock.sendall(message.encode('utf-8'))
        

    def write_sock(self, sock):
        '''
        Client writes a message that will be sent via client-server to other clients
        in the chat.
        '''
        while True:
            txt = str(input(''))
            if txt == '':
                print (self.client_name+" is leaving chat. Goodbye")
            byte_len = "Length: "+str(len(txt.encode('utf-8')))
            self.send_msg(sock, byte_len, txt)
        sock.close()

    def read_sock(self, sock):
        '''
        Client constantly receives and reads messages from other clients in the chat
        via client-server socket.
        '''
        bin_reply = b""
        while True:
            more = sock.recv(4096)
            if more == b'':
                sock.close()
                sys.exit(1)
            bin_reply += more
            print (more.decode('utf-8'))
        sock.close()


def main():

    print (sys.argv, len(sys.argv))
    client_name = str(sys.argv[1])
    chat_host =  str(sys.argv[2])
    chat_port = int(sys.argv[3])
    chat_client = ChatClient(chat_host, chat_port, client_name)


if __name__ == '__main__':
    main()
