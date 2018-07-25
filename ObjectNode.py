import ipfsapi
import json
import io

IPFS_IP = '127.0.0.1'
IPFS_PORT = 5001

class ObjectNode:
    def __init__(self):
        self.api = ipfsapi.connect(IPFS_IP,IPFS_PORT)
        self.ObjectHash = "NULL"

    def new(self, UserID):
        Tbyte = bytes(json.dumps({"Data":UserID}))
        self.ObjectHash = self.api.object_put(io.BytesIO(Tbyte))['Hash']
        self.api.pin_add(self.ObjectHash)

    def load(self, Fhash):
        self.ObjectHash = Fhash

    def GetObjectInfo(self):
        return self.api.object_get(self.ObjectHash)

    def AddHash(self,ObjectName,Fhash):
        self.ObjectHash = self.api.object_patch_add_link(self.ObjectHash,ObjectName,Fhash)['Hash']
        self.api.pin_add(self.ObjectHash)


#Jres = api.object_get("QmQQa3HUgDtXzwwBcdcwsSVPWWJ7PVWc8UmbADV1FhxB8n")
#Jres = json.loads(res)
#data = Jres['Data']
#Links = Jres['Links']

#print(Links)
