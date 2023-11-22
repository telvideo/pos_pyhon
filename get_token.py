import datetime
import json
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
import requests
import base64
import time
from normalizer_invoice import normalizer

mil_time = int(time.time() * 1000) 

url = "https://sandboxrc.tax.gov.ir/req/api/self-tsp/sync/GET_TOKEN"  # API url 

headers= {'requestTraceId':f'{mil_time}', 'timestamp': f'{mil_time}', 'Content-Type':'application/json'}
dict_headers= {'requestTraceId':f'{mil_time}', 'timestamp': f'{mil_time}'}


dict_packet= {
"uid":'null',
"packetType":"GET_TOKEN",
"retry":'false',
"data":{"username":"Axxxxx"},
"encryptionKeyId":"",
"symmetricKey":"",
"iv":"",
"fiscalId":"",
"dataSignature":""
}
def get_tocken():
  dict3 = {**dict_headers, **dict_packet}  # Merging two dictionaries 
  print("dict3=>>>",dict3)
  normalize = normalizer_jason(dict3)
  key = RSA.import_key(open('rsa.private').read()) # Get the private key
  h = SHA256.new(normalize.encode('utf-8'))
  signature = pkcs1_15.new(key).sign(h)  # Sign the packet
  base64_bytes = base64.b64encode(signature) 
  base64_signature = base64_bytes.decode('ascii')

  null = None
  false = False
  paket_for_send ={
  "time": 1,
    "packet": {
      "uid": null,
      "packetType": "GET_TOKEN",
      "retry": false,
      "data": {
        "username": "Axxxxx"
      },
      "encryptionKeyId": "",
      "symmetricKey": "",
      "iv": "",
      "fiscalId": "",
      "dataSignature": ""
    },
     "signature":  f"{base64_signature}"
  }

  r= requests.post(url, data= json.dumps(paket_for_send), headers = headers  ,verify=False)


  if r.status_code == 200:
    print("Success!")
    print(r)
    print("responce==", r.text)
    return json.loads(r.text)['result']['data']['token'] , json.loads(r.text)['timestamp']
  else:
    print(f"Error: {r.text}")
   
x= get_tocken()
print('Tocken: ',x)
