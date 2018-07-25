import ipfsapi
import json
import io

IPFS_IP = '127.0.0.1'
IPFS_PORT = 5001

class ObjectNode:
    def __init__(self):
        self.api = ipfsapi.connect(IPFS_IP,IPFS_PORT)
        self.ObjectHash = "NULL"
        self.ObjectMatch = dict()

    def new(self, UserID):
        Tbyte = bytes(json.dumps({"Data":UserID}))
        self.ObjectHash = self.api.object_put(io.BytesIO(Tbyte))['Hash']
        self.api.pin_add(self.ObjectHash)

    def load(self, Fhash):
        self.ObjectHash = Fhash

    def match(self, ObjectName):
        Tbyte = bytes(json.dumps({"Data":ObjectName}))
        Thash = self.api.object_put(io.BytesIO(Tbyte))['Hash']
        self.api.pin_add(Thash)
        self.ObjectMatch[ObjectName] = Thash
        self.ObjectMatch[Thash] = ObjectName

    def GetObjectInfo(self):
        Tdict = self.api.object_get(self.ObjectHash)
        return Tdict

    def GetInfo(self):
        Tdict = self.api.object_get(self.ObjectHash)
        Rdict = dict()
        Rdict["Data"] = Tdict["Data"]
        for x in Tdict["Links"]:
            kv = json.loads(x["Name"])
            for y in kv:
                Rdict[y] = kv[y]
        return Rdict

    def GetInfo2(self):
        Rlist = list()
        Tdict = self.api.object_get(self.ObjectHash)
        for x in Tdict["Links"]:
            T1dict = self.api.object_get(x["Hash"])
            Rdict = dict()
            Rdict["Data"] = T1dict["Data"]
            for y in T1dict["Links"]:
                kv = json.loads(y["Name"])
                for z in kv:
                    Rdict[z] = kv[z]
            Rlist.append(Rdict)
        return Rlist

    def AddHash(self,ObjectName,Fhash):
        self.ObjectHash = self.api.object_patch_add_link(self.ObjectHash,ObjectName,Fhash)['Hash']
        self.api.pin_add(self.ObjectHash)

    def RemoveHash(self,ObjectName):
        OldOhash = self.ObjectHash
        self.ObjectHash = self.api.object_patch_rm_link(self.ObjectHash,ObjectName)['Hash']
        self.api.pin_add(self.ObjectHash)
        self.api.pin_rm(OldOhash)
        self.api.repo_gc()

    def AddField(self,field,value):
        if field not in self.ObjectMatch:
            self.match(field)
        self.AddHash(json.dumps({field:value}),self.ObjectMatch[field])

    def RemoveField(self,field):
        if field not in self.ObjectMatch:
            return "FIELD NOT EXIST."
        Tdict = self.api.object_get(self.ObjectHash)
        for x in Tdict["Links"]:
            kv = json.loads(x["Name"])
            if field in kv.keys():
                aa = (json.dumps({field:kv[field]}))
                self.RemoveHash(aa)

    def AddRow(self,row):
        for x in row:
            self.AddField(x,row[x])
