from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
import base64

def normal_signature_invoice(packet_normalaised):
    key = RSA.import_key(open('rsa.private').read())
    h = SHA256.new(packet_normalaised.encode('utf-8'))
    signature = pkcs1_15.new(key).sign(h)
    base64_bytes = base64.b64encode(signature)
    base64_signature = base64_bytes.decode('ascii')
    return  base64_signature
