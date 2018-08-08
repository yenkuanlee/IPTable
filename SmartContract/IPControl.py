# -*- coding: utf-8 -*-
import getpass
import json
from web3 import Web3, HTTPProvider, TestRPCProvider
import os
import psycopg2

class IPControl:
    def __init__(self, _host,_account):
        Cpath = os.path.dirname(os.path.realpath(__file__))
        f = open(Cpath+'/iptable.json','r')
        line = f.readline()
        Jline = json.loads(line)
        f.close()
        abi = Jline['abi']
        contract_address = Jline['contract_address']

        self.host = _host
        self.account = _account
        self.passwd = getpass.getpass('Password:')
        self.w3 = Web3(HTTPProvider('http://'+self.host+':8545'))
        self.account = self.w3.toChecksumAddress(self.account)
        self.w3.eth.defaultAccount = self.account
        check_passwd = self.w3.personal.unlockAccount(self.account,self.passwd)
        if not check_passwd :
            print("Wrong password, failed to log in.")
            exit(0)
        self.contract_instance = self.w3.eth.contract(abi=abi, address=contract_address)

        self.conn = psycopg2.connect(database="postgres",user="postgres",host="127.0.0.1", port="5432")
        self.cur = self.conn.cursor()

    def GetSchema(self):
        return self.contract_instance.functions.GetSchema().call()
        
    def GetInfo(self):
        return self.contract_instance.functions.GetInfo().call()

    def GetShardInfo(self,Sman):
        Sman = self.w3.toChecksumAddress(Sman)
        result = self.contract_instance.functions.GetShardInfo(Sman).call()
        Odict = dict()
        Odict["RowCount"] = result[0]
        Odict["Description"] = result[1]
        return json.dumps(Odict)

    def GetSaleList(self):
        result =  self.contract_instance.functions.GetSaleList().call()
        return result

    def Buy(self,Sman):
        self.contract_instance.functions.Buy(Sman).transact({'from': self.account})

    def ShowPocket(self):
        result =  self.contract_instance.functions.ShowPocket().call()
        return result

    def GetPocketShardInfo(self,TSID):
        Odict = dict()
        result = self.contract_instance.functions.GetPocketShardInfo(TSID).call()
        try:
            Odict['TSID'] = result[0]
            Odict['owner'] = result[1]
            Odict['rowCount'] = result[2]
            Odict['description'] = result[3]
            Odict['fhash'] = result[4]
        except:
            pass
        return Odict

    def CommitFhash(self,Fhash):
        self.contract_instance.functions.commitFhash(Fhash).transact({'from': self.account})

    def PushShard(self,rcnt,dct):
        self.contract_instance.functions.pushShard(rcnt,dct).transact({'from': self.account})

    def CreateTable(self, table_name):
        TSID = "(tsid bigint, "
        schema = self.GetSchema()
        schema = schema.replace("(",TSID)
        SQL = "CREATE FOREIGN TABLE IF NOT EXISTS "+table_name+schema+"SERVER ipserver OPTIONS(table_name '"+table_name+"');"
        self.cur.execute(SQL)
        self.conn.commit()        

    def CreateTable(self,table_name,TTSID):
        fhash = self.GetPocketShardInfo(TTSID)['fhash']
        TSID = "(tsid bigint, "
        schema = self.GetSchema()
        schema = schema.replace("(",TSID)
        SQL = "CREATE FOREIGN TABLE IF NOT EXISTS "+table_name+schema+"SERVER ipserver OPTIONS(table_name '"+table_name+"', fhash '"+fhash+"');"
        self.cur.execute(SQL)
        self.conn.commit()

    def CommitShard(self,table_name):
        try:
            self.cur.execute("SELECT FHASH FROM _lookup WHERE table_name = '"+table_name+"';")
            fhash = self.cur.fetchone()[0]
            self.CommitFhash(fhash)
        except Exception as e:
            print(e)
            print("NO UPLOAD")
