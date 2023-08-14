import json
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
import requests
import base64
import time
from normal_json import normalizer_jason
# from get_token import get_tocken



mil_time = int(time.time() * 1000) 


url = "https://sandboxrc.tax.gov.ir/req/api/self-tsp/sync/GET_SERVER_INFORMATION/"



# token_t= get_tocken()
token_t= "eyJhbGciOiJIUzUxMiJ9.eyJjbGllbnRUeXBlIjoiTUVNT1JZIiwidG9rZW5JZCI6Ijg1ODgyMTU1LTJmZTUtNGZkNy05ZjU4LTgzNzJkZjIxN2UyMyIsInBlcm1pc3Npb25zIjpbInNlbGYtdHNwLmFzeW5jLmZhc3QtZW5xdWV1ZSIsInNlbGYtdHNwLnN5bmMiLCJzZWxmLXRzcC5hc3luYy5ub3JtYWwtZW5xdWV1ZSJdLCJwYWNrZXRUeXBlcyI6WyJHRVRfRUNPTk9NSUNfQ09ERV9JTkZPUk1BVElPTiIsIklOUVVJUllfQllfVElNRSIsIkdFVF9TRVJWRVJfSU5GT1JNQVRJT04iLCJJTlFVSVJZX0JZX1VJRCIsIklOUVVJUllfQllfUkVGRVJFTkNFX05VTUJFUiIsIkdFVF9UT0tFTiIsIkdFVF9GSVNDQUxfSU5GT1JNQVRJT04iLCJJTlZPSUNFLlYwMSIsIklOUVVJUllfQllfVElNRV9SQU5HRSIsIkdFVF9TRVJWSUNFX1NUVUZGX0xJU1QiXSwiaXNzIjoiVEFYIE9yZ2FuaXphdGlvbiIsImlkIjoiQTExMTIyIiwiZXhwIjoxNjc5MjI1NjkzLCJ0YXhwYXllcklkIjoiNjA3ZWQ2MDctOTNmYi00YTA0LTkxN2EtMWQ4M2ZmNjEwM2U5IiwiY3JlYXRlRGF0ZSI6MTY3OTIxMTI5MzU1MX0.aeL-i3Y2xab2MbZ2QVbDaK7YIwMHZ95YpFdsSBs6psziuIXUz1u5S1M0Oq4b5Xtu_CRhvkR9BElJJH9NQlD8uA"

headers= {'requestTraceId':f'{mil_time}', 'timestamp': f'{mil_time}',  'Authorization':f'{"Bearer " +token_t}','Content-Type':'application/json'}
dict_headers= {'requestTraceId':f'{mil_time}', 'timestamp': f'{mil_time}'}


dict_packet= {
"uid":'null',
"packetType":"GET_SERVER_INFORMATION",
"retry":'false',
"data":'null',
"encryptionKeyId":"",
"symmetricKey":"",
"iv":"",
"fiscalId":"",
"dataSignature":""
}

dict3 = {**dict_headers, **dict_packet}  
print('Get_ficcall=',dict3)
normalize = normalizer_jason(dict3)
# print(normalize)
# Get private key
key = RSA.import_key(open('rsa.private').read())
h = SHA256.new(normalize.encode('utf-8'))
signature = pkcs1_15.new(key).sign(h)
# print(signature)
# # signature_bytes = signature.encode('ascii')
base64_bytes = base64.b64encode(signature)
base64_signature = base64_bytes.decode('ascii')
# print(base64_signature)


null = None
false = False
paket_for_send = {
    "time": mil_time,
    "packet": {
        "uid": null,
        "packetType": "GET_SERVER_INFORMATION",
        "retry": false,
        "data": null,
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
print("responce==",r.text)
print('headers ==>', r.request.headers)
print('body ==>', r.request.body)


