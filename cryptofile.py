"""File like object for auto encrypting and decrypting using RSA keys"""
import io

# from Crypto import Random
# from Crypto.PublicKey import RSA
#
# def generate_keys():
#     modulus_length = 256*4
#     privatekey = RSA.generate(modulus_length, Random.new().read)
#     publickey = privatekey.publickey()
#     return privatekey, publickey


class EncryptedFile(io.FileIO):
    """File like object automatic encryptes and decryptes data for file"""
    def write(self, b, public_key):
        """Write with encryption"""
        encr_b = self.encrypt(b, public_key)
        super().write(encr_b)

    def writelines(self, lines, public_key):
        encr_lines = []
        for line in lines:
            encr_lines.append(self.encrypt(line, public_key))
        super().writelines(encr_lines)

    def read(self, size, private_key):
        """Read with decryption"""
        encr_b = super().read(size)
        return self.decrypt(encr_b, private_key)

    @staticmethod
    def encrypt(b, public_key):
        """Encryptes b using public key"""
        encr_b = public_key.encrypt(b, None)[0]
        return encr_b

    @staticmethod
    def decrypt(encr_b, private_key):
        """Decryptes encr_b using private key"""
        b = private_key.decrypt(encr_b)
        return b

# pr, pub = generate_keys()
# with EncryptedFile('a', 'w+') as file:
#     file.write(b"sda", public_key=pub)
#     file.seek(0,0)
#     s = file.read(None, private_key=pr)
#     print(s)
