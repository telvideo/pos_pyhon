import pyaes, pbkdf2, binascii, os, secrets

# Derive a 256-bit AES encryption key from the password


password = "s3cr3t*c0d3"
passwordSalt = os.urandom(16)
key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
print('AES encryption key:', binascii.hexlify(key))



# iv = secrets.randbits(256)
# print(hexlify(iv))




# secretKey = os.urandom(32)  # 256-bit random encryption key
# print("Encryption key:", binascii.hexlify(secretKey))
# b'63d52e9c81390d8b77fd4bd3a2800ccbeb8481b84193ec99f7483353a645e841'
