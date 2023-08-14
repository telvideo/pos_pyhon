import base64
import binascii
import json


from Cryptodome import Random
from Cryptodome.Cipher import AES
from secrets import token_bytes
from base64 import b64encode
import binascii
import json
from nltk import flatten

def xor_creator(AES_key,invoice):

    # Remove spaces in json dictionary and convert to bytes
    str_json =invoice
    invoice_str = json.dumps(str_json, ensure_ascii=False, separators=(',', ':'))
    str_json_byte = bytes(invoice_str, encoding='UTF-8').decode()


    def bytes2binstr(b, n=None): ## byte to bit bill dict
        s = ' '.join(f'{x:08b}' for x in b.encode('UTF-8'))
        return s if n is None else s[:n + n // 8 + (0 if n % 8 else -1)]
    bit_arry_packet = bytes2binstr(str_json_byte).split(' ')
    # bit_arry_packet = bytes2binstr(str_string_test_normalized).split(' ')


    # The bit list here is converted to base two integer value one by one for better understanding

    def mabna_2(bit_arry):
        arry_2 = []
        for i in range(len(bit_arry)):
            arry_2.append(int(bit_arry[i], 2))
        return arry_2




    # Dividing the bitized bill into 32 blocks, which means that each block is 256 bits
    split_size = 32
    arry_mabna_2_packet = mabna_2(bit_arry_packet)
    splitted_list_mabna_2_packet = [arry_mabna_2_packet[i:i+split_size] for i in range(0, len(arry_mabna_2_packet), split_size)]



    key=AES_key

    AES_key_byte =bytes.fromhex(key)

    def key_bytes2binstr(b, n=None): ## byte to bit key
        s = ' '.join(f'{x:08b}' for x in b)
        return s if n is None else s[:n + n // 8 + (0 if n % 8 else -1)]

    key_bit_arry = key_bytes2binstr(AES_key_byte).split(' ')
    key_bit_arry_mabna_2 = mabna_2(key_bit_arry)



    ###########XOR#############XOR##XOR##########XOR#############
    from operator import xor
    XOR_list=[]
    for k in range(len(splitted_list_mabna_2_packet)):
        if len(splitted_list_mabna_2_packet[k]) == len(key_bit_arry_mabna_2):
            XOR_list.append([splitted_list_mabna_2_packet[k][index] ^ key_bit_arry_mabna_2[index] for index in range(len
                                                                                    (splitted_list_mabna_2_packet[k]))])
        else:
            len_last =len(splitted_list_mabna_2_packet[k])
            XOR_list.append([splitted_list_mabna_2_packet[k][index] ^ key_bit_arry_mabna_2[:len_last][index]
                                                    for index in range(len(splitted_list_mabna_2_packet[k]))])

    xor_lis_flat = flatten(XOR_list)
    return xor_lis_flat

###########XOR#############XOR##XOR##########XOR#############


PASSPHRASE_STRING = '4fda3c622e966e0839441401bbd3b8f191d4267bf5f19b40812a34b212fd3ed9'
PASSPHRASE = b'4fda3c622e966e0839441401bbd3b8f191d4267bf5f19b40812a34b212fd3ed9' # In the document
iv = b'4fda3c622e966e0839441401bbd3b8f191d4267bf5f19b40812a34b212fd3ed9' # In the document


def AES_encrypt(data, iv):
    global PASSPHRASE
    data_byte = bytes(data)
    key = binascii.unhexlify(PASSPHRASE)
    cipher = AES.new(key, AES.MODE_GCM, binascii.unhexlify(iv))
    x, t = cipher.encrypt_and_digest(data_byte)
    cipher_tag = x + t
    cipher_tag_decode =base64, b64encode(cipher_tag).decode()

    return cipher_tag_decode[1]



















