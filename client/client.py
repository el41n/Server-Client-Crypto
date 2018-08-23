import logging
import pickle
import socket
import uuid

from Crypto.PublicKey import RSA

from cryptofile import EncryptedFile


logging.basicConfig(level=logging.DEBUG)


class Client:
    def __init__(self):
        self.IP = '127.0.0.1'
        self.PORT = 8005
        self.BUFFER_SIZE = 1024
        self.KEY_MESSAGE = b"GIVE_ME_A_KEY"
        self.FILE_TRANSFER_MESSAGE = b"READ_A_FILE"
        self.file_name = "/tmp/" + str(uuid.uuid1())
        self.file_name = self.file_name.encode()
        self.public_key = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.u_input = ''

    def start(self):
        self.user_input()
        try:
            self.sock.connect((self.IP, self.PORT))
            self.get_public_key()

            with EncryptedFile(self.file_name, 'w') as file:
                logging.debug('Writing user input to file')
                file.write(self.u_input.encode(), public_key=self.public_key)

            self.send_file_name()

        except socket.error as err:
            logging.debug(str(err))
        finally:
            self.sock.close()

    def get_public_key(self):
        logging.debug('Getting public key')
        self.sock.send(self.KEY_MESSAGE)
        self.public_key = self.sock.recv(self.BUFFER_SIZE)
        self.public_key = RSA.importKey(self.public_key, passphrase=None)

    def send_file_name(self):
        logging.debug('Sending file name')
        self.sock.send(self.FILE_TRANSFER_MESSAGE)
        accept = self.sock.recv(self.BUFFER_SIZE)
        if accept == b'OK':
            self.sock.send(self.file_name)

    def user_input(self):
        logging.debug('Wait for user input')
        print("Please enter text. Double enter for exit.")
        while True:
            line = input()
            if line == '':
                break
            self.u_input += line + '\n'


# s.connect((TCP_IP, TCP_PORT))
# s.send(bytes(MESSAGE, 'utf-8'))
# data = s.recv(BUFFER_SIZE)
# print(data)
# s.close()

if __name__ == '__main__':
    client = Client()
    client.start()
