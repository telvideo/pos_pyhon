from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
import base64

from Cryptodome.Hash import SHA256 


def aes_key_encryptions(aes_key_byte):
    key = RSA.import_key(open('tax_rsa.public').read())
    cipher= PKCS1_OAEP.new(key,hashAlgo=SHA256.new()) 
    signature =cipher.encrypt(aes_key_byte)
    base64_bytes = base64.b64encode(signature)
    base64_signature = base64_bytes.decode('ascii')
    return base64_signature
