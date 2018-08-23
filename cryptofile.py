import io
import uuid

from Crypto import Random
from Crypto.PublicKey import RSA

def generate_keys():
    # RSA modulus length must be a multiple of 256 and >= 1024
    modulus_length = 256*4 # use larger value in production
    privatekey = RSA.generate(modulus_length, Random.new().read)
    publickey = privatekey.publickey()
    return privatekey, publickey

class EncryptedFile(io.FileIO):
    def write(self, b, public_key):
        super().write(self.encrypt(b, public_key))

    def read(self, size, private_key):
        encr_b = super().read(size)
        return self.decrypt(encr_b, private_key)

    def encrypt(self, b, public_key):
        encr_b = public_key.encrypt(b, 32)[0]
        return encr_b

    def decrypt(self, encr_b, private_key):
        b = private_key.decrypt(encr_b)
        return b

# pr, pub = generate_keys()
# with EncryptedFile('a', 'w+') as file:
#     file.write(b"sda", public_key=pub)
#     file.seek(0,0)
#     s = file.read(None, private_key=pr)
#     print(s)