import logging
import socket

from Crypto import Random
from Crypto.PublicKey import RSA

from cryptofile import EncryptedFile

logging.basicConfig(level=logging.DEBUG)


class Server:
    def __init__(self):
        self.IP = '127.0.0.1'
        self.PORT = 8005
        self.BUFFER_SIZE = 1024

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.IP, self.PORT))

        self.dispatcher = {b"GIVE_ME_A_KEY": self.send_public_key,
                           b"READ_A_FILE": self.get_file_name, }

        self.file_name = None
        self.public_key = None
        self.private_key = None
        self.generate_keys()

    def start(self):
        logging.debug('Server starts')
        self.server.listen(1)
        try:
            conn, address = self.server.accept()
            logging.debug('Connected {}, {}'.format(address[0], address[1]))
            data = True
            while data:
                logging.debug('receiving')
                data = conn.recv(self.BUFFER_SIZE)

                if data in self.dispatcher:
                    self.dispatcher[data](conn)
                logging.debug('received data {}'.format(str(data, encoding='utf-8')))
        except socket.error as err:
            logging.debug(str(err))
        finally:
            conn.close()
            logging.debug('Connection closes')

    def send_public_key(self, conn):
        logging.debug('Sending public key')
        conn.send(self.public_key.exportKey(format='PEM', passphrase=None, pkcs=1))

    def get_file_name(self, conn):
        logging.debug('Receiving file name')
        conn.send(b"OK")
        self.file_name = conn.recv(self.BUFFER_SIZE)
        self.read_file()

    def generate_keys(self):
        logging.debug('Generating keys')
        self.private_key = RSA.generate(256*4, Random.new().read)
        self.public_key = self.private_key.publickey()

    def read_file(self):
        with EncryptedFile(self.file_name) as file:
            logging.debug("Reading file")
            text = file.read(None, private_key=self.private_key)
            print(str(text, 'utf-8)'))


if __name__ == '__main__':
    server = Server()
    server.start()
