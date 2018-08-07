# -*- coding: utf-8 -*-
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
        self.passwd = '123'
        self.w3 = Web3(HTTPProvider('http://'+self.host+':8545'))
        self.account = self.w3.toChecksumAddress(self.account)
        self.w3.personal.unlockAccount(self.account,self.passwd)
        self.contract_instance = self.w3.eth.contract(abi=abi, address=contract_address)

        self.conn = psycopg2.connect(database="postgres",user="postgres",host="127.0.0.1", port="5432")
        self.cur = self.conn.cursor()

    def GetSchema(self):
        return self.contract_instance.functions.GetSchema().call()
        
    def GetInfo(self):
        return self.contract_instance.functions.GetInfo().call()

    def SetShard(self,Ehash):
        self.contract_instance.functions.setShard(Ehash).transact({'from': self.account})

    def CreateTable(self):
        schema = self.GetSchema()
        self.cur.execute(schema)
        self.conn.commit()        
        

'''

# Contract instance in concise mode
contract_instance = w3.eth.contract(abi=abi, address=contract_address)

#contract_instance.functions.setShard(Ehash).transact({'from': account})
#print(contract_instance.functions.GetInfo().call())
print(contract_instance.functions.GetSchema().call())
'''
