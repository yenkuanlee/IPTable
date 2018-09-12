import json
import requests
headers = {'X-IOTA-API-Version': '1'}
GetTag = {"command": "findTransactions", "tags": ["KEVIN999IS999HANDSOME"]}
def call_iota_api(f):
    r = requests.post("http://140.116.247.117:14265", data=json.dumps(f), headers=headers)
    return r.text

print(call_iota_api(GetTag))
