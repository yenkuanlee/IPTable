import base64
import iota
from iota import TryteString
import json
import psycopg2

class IOTATransaction:
    def __init__(self):
        self.FinalBundle = "INIT"
        self.TransactionHashList = list()
        #self.api = iota.Iota("https://field.deviota.com:443")
        self.api = iota.Iota("http://140.116.247.117:14265")
    def MakePreparingTransaction(self, TargetAddress, StringMessage, tag='KEVIN999IS999HANDSOME'):
        TargetAddress = str.encode(TargetAddress)
        pt = iota.ProposedTransaction(address = iota.Address(TargetAddress),message = iota.TryteString.from_unicode(StringMessage),tag = iota.Tag(str.encode(tag)),value=0)
        return pt
    def SendTransaction(self, PTList, dep=3, mwm=14):
        FinalBundle = self.api.send_transfer(depth=dep,transfers=PTList,min_weight_magnitude=mwm)['bundle']
        self.FinalBundle = FinalBundle
        for txn in FinalBundle:
            Vtxn = vars(txn)
            if Vtxn['hash'] not in self.TransactionHashList:
                self.TransactionHashList.append(Vtxn['hash'])
        
    def GetTransactionFinalBundleHash(self):
        return self.FinalBundle.hash
    def GetTransactionFinalBundle(self):
        return self.FinalBundle
    def GetTransactionHash(self):
        return self.TransactionHashList
    def GetTransactionMessage(self, TID):
        bundle = self.api.get_bundles(TID)
        for x in bundle['bundles']:
            for txn in x:
                Vtxn = vars(txn)
                if Vtxn['hash'] != TID:
                    continue
                TryteStringMessage = str(Vtxn['signature_message_fragment'])
                return TryteString(str.encode(TryteStringMessage)).decode()

    def Kencode(self,key, clear):
        enc = []
        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc).encode()).decode()
    def Kdecode(self,key, enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)

    def GetFhash(self, table_name):
        conn = psycopg2.connect(database="postgres",user="postgres",host="127.0.0.1", port="5432")
        cur = conn.cursor()
        cur.execute("SELECT FHASH FROM _lookup WHERE table_name = '"+table_name+"';")
        EncodeFhash = self.Kencode('KEVIN',cur.fetchone()[0])
        #try:
        return EncodeFhash
        #except Exception as e:
        #    return {"status":"ERROR", "log":str(e)}
    def CreateTable(self,table_name, TID):
        try:
            fhash = self.Kdecode('KEVIN',Jinfo['fhash'])
            Jinfo = json.loads(self.GetTransactionMessage(TID))
            sql = "CREATE FOREIGN TABLE "+table_name+Jinfo['table_schema']+"SERVER ipserver OPTIONS (table_name '"+table_name+"', fhash '"+Jinfo['fhash']+"');"
            conn = psycopg2.connect(database="postgres",user="postgres",host="127.0.0.1", port="5432")
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            return {"status": "SUCCESS"}
        except Exception as e:
            return {"status": "ERROR", "log": str(e)}
