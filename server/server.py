import logging
import socket
import threading


class Server:
    def __init__(self):
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 8004
        self.BUFFER_SIZE = 1024
        self._connection = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.TCP_IP, self.TCP_PORT))
        self.server.listen()

    def start(self):
        handlers = []
        while True:
            conn, address = self.server.accept()
            print('Connected {}, {}'.format(address[0], address[1]))
            #new_handler = threading.Thread(target=self.handle)
            while True:
                data = conn.recv(2)
                print('receiving')
                if not data:
                    break
                print(data)
            if data == b"OK":
                print("recognized")
            print('received data', data)
            conn.close()

if __name__ == '__main__':
    server = Server()
    server.start()
