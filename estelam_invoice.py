import json
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
import requests
import base64
import time
from normal_json import normalizer_jason
from get_token import get_tocken
from send_invoise import send_invoice


mil_time = int(time.time() * 1000)


# url = "https://sandboxrc.tax.gov.ir/req/api/tsp/sync/INQUIRY_BY_UID"
url = "https://sandboxrc.tax.gov.ir/req/api/self-tsp/sync/INQUIRY_BY_REFERENCE_NUMBER"




token_t = "eyJhbGciOiJIUzUxMiJ9.eyJjbGllbnRUeXBlIjoiTUVNT1JZIiwidG9rZW5JZCI6IjZhYzBiNmY4LWQ2OGItNGZjMC04ZmM3LWIxNzIxNDc1ODNiMiIsInBlcm1pc3Npb25zIjpbInNlbGYtdHNwLmFzeW5jLmZhc3QtZW5xdWV1ZSIsInNlbGYtdHNwLnN5bmMiLCJzZWxmLXRzcC5hc3luYy5ub3JtYWwtZW5xdWV1ZSJdLCJwYWNrZXRUeXBlcyI6WyJHRVRfRUNPTk9NSUNfQ09ERV9JTkZPUk1BVElPTiIsIklOUVVJUllfQllfVElNRSIsIkdFVF9TRVJWRVJfSU5GT1JNQVRJT04iLCJJTlFVSVJZX0JZX1VJRCIsIklOUVVJUllfQllfUkVGRVJFTkNFX05VTUJFUiIsIkdFVF9UT0tFTiIsIkdFVF9GSVNDQUxfSU5GT1JNQVRJT04iLCJJTlZPSUNFLlYwMSIsIklOUVVJUllfQllfVElNRV9SQU5HRSIsIkdFVF9TRVJWSUNFX1NUVUZGX0xJU1QiXSwiaXNzIjoiVEFYIE9yZ2FuaXphdGlvbiIsImlkIjoiQTExMTIyIiwiZXhwIjoxNjg0NzkzMjc1LCJ0YXhwYXllcklkIjoiNjA3ZWQ2MDctOTNmYi00YTA0LTkxN2EtMWQ4M2ZmNjEwM2U5IiwiY3JlYXRlRGF0ZSI6MTY4NDc3ODg3NTczOH0.zdRG2G6kGyBcTGc24hmuXQxhWhv8f9JKfeyXDo8_1oFUrx49HePOdCNwC7czWtvrZKdyj5_NgC2gQFij-bdsEQ"

headers= {'requestTraceId':f'{mil_time}', 'timestamp': f'{mil_time}',  'Authorization':f'{"Bearer " +token_t}','Content-Type':'application/json'}

dict_headers= {'requestTraceId':f'{mil_time}', 'timestamp': f'{mil_time}'}





fiscal_id="Axxxxx"
ref_id = send_invoice()
normal_estelam= f"{token_t}#{ref_id}#########INQUIRY_BY_REFERENCE_NUMBER#{mil_time}#false###{mil_time}##"  #normal packet
key = RSA.import_key(open('rsa.private').read())
h = SHA256.new(normal_estelam.encode('utf-8'))
signature = pkcs1_15.new(key).sign(h)
base64_bytes = base64.b64encode(signature)
base64_signature = base64_bytes.decode('ascii')


null = None
false = False


paket_for_send= {
  "time": int(time.time() * 1000),
  "packet": {
    "uid": null,
    "packetType": "INQUIRY_BY_REFERENCE_NUMBER",
    "retry": false,
    "data": {
      "referenceNumber": [
        f"{ref_id}"
      ]
    },
    "encryptionKeyId": "",
    "symmetricKey": "",
    "iv": "",
    "fiscalId": "",
    "dataSignature": ""
  },
  "signature": f"{base64_signature}"
}









r= requests.post(url, data= json.dumps(paket_for_send), headers = headers , verify=False )
print(r)
print(r.text)
estelom_json= json.loads(r.text)

status = estelom_json["result"]["data"][0]["status"]
print("status",status)
if status == "PENDING":
  with open('status.txt', 'a') as f:
    f.write('\n'.join(estelom_json["result"]["data"][0]["referenceNumber"]))


