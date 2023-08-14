import json
import time
import uuid
import requests
from Normal_Signature_Invoice import normal_signature_invoice
from AES_Bills_encryptions import xor_creator,AES_encrypt
from get_token import get_tocken
from aes_key_encryptions import aes_key_encryptions
import json
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
import base64
from normalizer_invoice import normalizer
from Input_invoice_user import input_invoice_user
import to_db
from to_db import invoice_to_db 


def send_invoice():
    

    json_load_invoice =input_invoice_user()
    print("میاد اینجا")
    print(json_load_invoice)
    save_to_db=invoice_to_db(json_load_invoice) # save_to_db
    print("save_to_db==",save_to_db)





    def packet_normalaised_signature(packet_normalaised):
        key = RSA.import_key(open('rsa.private').read())
        h = SHA256.new(packet_normalaised.encode('utf-8'))
        signature = pkcs1_15.new(key).sign(h)
        base64_bytes = base64.b64encode(signature)
        base64_signature = base64_bytes.decode('ascii')

        return base64_signature

    mil_time = int(time.time() * 1000) 


    normal_invoice= normalizer(json_load_invoice)

    print("normal_invoice:==",normal_invoice)
    AES_key='4fda3c622e966e0839441401bbd3b8f191d4267bf5f19b40812a34b212fd3ed9' 
    AES_key_btye=b'4fda3c622e966e0839441401bbd3b8f191d4267bf5f19b40812a34b212fd3ed9' 
    iv="4fda3c622e966e0839441401bbd3b8f191d4267bf5f19b40812a34b212fd3ed9" 

    data_xor = xor_creator(AES_key,json_load_invoice)
    data_aes_evcrypt= AES_encrypt(data_xor,iv)
    token_t = get_tocken()[0]
    data =data_aes_evcrypt


    dataSignature= normal_signature_invoice( normal_invoice )
    encryptionKeyId="6a2bcd88-a871-4245-a393-2843eafe6e02"
    fiscalId="Axxxxx"
    packetType="INVOICE.V01"
    symmetricKey="O2hxAEYrYvtPvLR+YeVhPtlPbp0Pnl0kJ5JRCIlvUepgHDCqqi5n5qY8gia5Qci1aLLgNu2Uq24YDGr2L13pA4prbqPSns1ugk52SVmekK/gSY+Ca98qm8QTcUzzhOouhIUOD5ivNj4QWOWqzwwTiD9ZR/Ii2O9G3vg1guOJacnVMWnZcS3Z8VUqUjfRdeCTObQryuh1apDzN6mfLzbTnfqKhv4NA/Y5RwapP+wsZJ/xsRiodngBOm9S7txLZuE+2jNxhww2oUAS6Gx34fLwwfQoDL0M397ujAY7aLmw5fMyLflXhTfn5ekHMLAnsd+3QnMwl8HYWD/egH/uI9+x7pMlNTag4EmgOKi1W+lcrwcvXszdubPuI09EIrA3NAlaT6FRGnAH+BLak7CBqKKVZBDlhK48VXMixTnSruD7ODXAyIJO4rzFvw+loZCP6Tu9E/HJV4TNmsCRAv7sJSCjPhYFCSKBBCsxiV/KZe/Q0oLyPhrN+ThYHxzJ27AGLyxgJLrwoLnUm9S61ujsRgNw7Mn4VHxdJ8fwzRNDC4mIpf5FrTy5ZHAFjCQ3OyXJWIS9hc5yxoLkgEI8xQ+pROu7hvEjvnF23kfw+TiYTJXOJHBqavA7RIN2XPiV0YOAeaVj3QswGDumW2k2EB7/Qm7n8TBIGhR4TMUauvOC8Occ8N4="
    uid =str(uuid.uuid4())
    requestTraceId=str(uuid.uuid4())
    retry =''
    retry1 ='''false'''
    timestamp =str(mil_time)
    int_timestamp =mil_time



    packet_normalaised =f"{token_t}#{data}#{dataSignature}#{encryptionKeyId}#{fiscalId}#{iv}#{packetType}###{symmetricKey}#{uid}#{requestTraceId}#{timestamp}"




    null =None
    false=False
    paket_for_send ={
     "time": 1,
      "packets": [
        {
          "uid": f"{uid}",
          "packetType": f"{packetType}",
          "retry": null,
          "data": f"{data}",
          "encryptionKeyId": f"{encryptionKeyId}",
          "symmetricKey": f"{symmetricKey}",
          "iv": f"{iv}",
          "fiscalId":f"{fiscalId}",
          "dataSignature":f"{dataSignature}"
        }
      ],
      "signature":f"{packet_normalaised_signature(packet_normalaised)}"
    }







    headers= {'requestTraceId':f'{requestTraceId}', 'timestamp': f'{int_timestamp}', 'Authorization':f'{"Bearer " +token_t}','Content-Type':'application/json'}
    url = "https://sandboxrc.tax.gov.ir/req/api/self-tsp/async/normal-enqueue"
    r= requests.post(url, data= json.dumps(paket_for_send), headers = headers, verify=False )
    return json.loads(r.text)["result"][0]["referenceNumber"]












































