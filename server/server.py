"""Server used for generating secret keys and read from encrypted file"""
import logging
import socket
import threading
import os

from Crypto import Random
from Crypto.PublicKey import RSA

from cryptofile import EncryptedFile

logging.basicConfig(level=logging.DEBUG)


class Server:
    """Listens to socket and waits for commands:
    -GIVE_ME_A_KEY - for sending public key to client
    -READ_A_FILE - for getting file name and read encrypted data from it"""
    def __init__(self):
        self.IP = '127.0.0.1'
        self.PORT = 8005
        self.BUFFER_SIZE = 1024

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server.bind((self.IP, self.PORT))

        self.dispatcher = {b"GIVE_ME_A_KEY": self.send_public_key,
                           b"READ_A_FILE": self.get_file_name, }

        self.public_key = None
        self.private_key = None
        self.generate_keys()

        self.threads = []
        self.is_on = True
        self.main_thread = threading.Thread(target=self.start)
        self.main_thread.start()

    def start(self):
        """Runs server"""
        logging.debug('Server starts')
        self.server.listen(1)
        while self.is_on:
            try:
                conn, address = self.server.accept()
                conn.setblocking(0)
            except socket.error:
                continue
            logging.debug('Connected %s, %d' % (address[0], address[1]))
            thr = threading.Thread(target=self.handle_connection, args=(conn,))
            self.threads.append(thr)
            thr.start()

    def stop(self):
        """Stops server"""
        self.is_on = False
        for thread in self.threads:
            thread.join()
        self.main_thread.join()

    def handle_connection(self, conn):
        """Thread based function for connection between server and client"""
        data = True
        while data:
            logging.debug('receiving')
            try:
                data = conn.recv(self.BUFFER_SIZE)
            except socket.error:
                continue
            if data in self.dispatcher:
                self.dispatcher[data](conn)
            logging.debug('received data %s' % (str(data, encoding='utf-8')))
        conn.close()
        logging.debug('Connection closes')

    def send_public_key(self, conn):
        """Used for exporting public key to client"""
        logging.debug('Sending public key')
        conn.send(self.public_key.exportKey(format='PEM', passphrase=None, pkcs=1))

    def get_file_name(self, conn):
        """Receives file name from client and runs decryption"""
        logging.debug('Receiving file name')
        conn.send(b"OK")
        while True:
            try:
                file_name = conn.recv(self.BUFFER_SIZE)
                break
            except socket.error:
                continue
        self.read_file(file_name)
        #os.remove(file_name)

    def generate_keys(self):
        """Generatees two RSA keys: public and private"""
        logging.debug('Generating keys')
        self.private_key = RSA.generate(256*4, Random.new().read)
        self.public_key = self.private_key.publickey()

    def read_file(self, file_name):
        """Opens EncryptFile and prints it text"""
        with EncryptedFile(file_name) as file:
            logging.debug("Reading file")
            text = file.read(None, private_key=self.private_key)
            print(str(text, 'utf-8)'))


if __name__ == '__main__':
    server = Server()
    input()
    server.stop()
