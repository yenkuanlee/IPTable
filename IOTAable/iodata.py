# -*- coding: UTF-8 -*-
import ipfsapi
import IOTATransaction
import json
import requests
import sys
import time

'''
A publish
B get_info
B request
A connect to B and send 0 transaction with data information
B create table with transaction ID
'''
# initial
a = IOTATransaction.IOTATransaction()
Ftag = 'IPTABLETEST'
api = ipfsapi.connect('127.0.0.1', 5001)
DontCareAddress = 'BXOM9LUNLPSEXBRJV9UUNLHSUHABEOGHQOGNBNBUEYSGOFZOEPYKEYRSFTXBOEJLUODUQXXGQ9NWQBSGH'

def call_iota_api(f):
    headers = {'X-IOTA-API-Version': '1'}
    r = requests.post("http://140.116.247.117:14265", data=json.dumps(f), headers=headers)
    return json.loads(r.text)

def Publish_IPTABLE(data_format, channel_tag, table_schema, table_rowCount, description, price, deadline, wallet_address):
    data_info = dict()
    data_info['data_format'] = data_format
    data_info['table_schema'] = table_schema
    data_info['table_rowCount'] = int(table_rowCount)
    data_info['description'] = description
    data_info['price'] = int(price)
    data_info['deadline'] = deadline
    data_info['wallet_address'] = wallet_address
    iotalent = IOTATransaction.IOTATransaction()
    try:
        pt = iotalent.MakePreparingTransaction(DontCareAddress, json.dumps(data_info), tag=channel_tag)
        iotalent.SendTransaction([pt])
        return {"status": "SUCCESS", "TID": iotalent.GetTransactionHash()}
    except Exception as e:
        return {"status": "ERROR", "location": "Function Publish", "log": str(e)}

def GetInfo(channel_tag):
    Tdict = dict()
    GetTag = {"command": "findTransactions", "tags": [channel_tag]}
    TransactionHashList = call_iota_api(GetTag)['hashes']
    iotalent = IOTATransaction.IOTATransaction()
    for x in TransactionHashList:
        Tdict[x] = iotalent.GetTransactionMessage(x)
    return Tdict

def Request(TID, wallet_address, channel_tag='IAMHUNGRY'):
    iotalent = IOTATransaction.IOTATransaction()
    Jinfo = json.loads(iotalent.GetTransactionMessage(TID))
    Rinfo = dict()
    Rinfo['target_ipfs_address'] = api.id()['Addresses']
    Rinfo['wallet_address'] = wallet_address
    try:
        pt = iotalent.MakePreparingTransaction(Jinfo['wallet_address'], json.dumps(Rinfo), tag=channel_tag, Ivalue=0) # Ivalue must > 0 in real case
        iotalent.SendTransaction([pt])
        return {"status": "SUCCESS", "TID": iotalent.GetTransactionHash()}
    except Exception as e:
        return {"status": "ERROR", "location": "Function Request", "log": str(e)}
         
def DataTransform_IPTABLE(TID, table_name, table_schema, description, table_rowCount):
    channel_tag = "IPTABLE999SO999COOL"
    iotalent = IOTATransaction.IOTATransaction()
    Jinfo = json.loads(iotalent.GetTransactionMessage(TID))
    table_info = dict()
    table_info['table_name'] = table_name
    table_info['table_schema'] = table_schema
    table_info['description'] = description
    table_info['table_rowCount'] = int(table_rowCount)
    try:
        for x in Jinfo['target_ipfs_address']:
            if '/ip6/' in x or '/127.0.0.1/' in x:
                continue
            api.swarm_connect(x)
        tmp = Jinfo['target_ipfs_address'][0].split("/")
        table_info['fhash'] = a.GetFhash(table_name,tmp[len(tmp)-1])
        pt = iotalent.MakePreparingTransaction(Jinfo['wallet_address'], json.dumps(table_info), tag=channel_tag)
        iotalent.SendTransaction([pt])
        return {"status": "SUCCESS", "TID": iotalent.GetTransactionHash()}
    except Exception as e:
        return {"status": "ERROR", "location": "Function Request", "log": str(e)}

def CreateIPTable(TID, table_name):
    iotalent = IOTATransaction.IOTATransaction()
    result = iotalent.CreateTable(table_name,TID)
    return result

try:
    do = sys.argv[1]
except:
    do = None

if do == 'publish':
    try:
        arg = sys.argv
        result = Publish_IPTABLE(arg[2],arg[3],arg[4],arg[5],arg[6],arg[7],arg[8],arg[9])
        print(result)
    except Exception as e:
        print({"status": "ERROR", "location": "do publish", "log": str(e)})
elif do == "get_info":
    try:
        result = GetInfo(sys.argv[2])
        print(json.dumps(result))
    except Exception as e:
        print({"status": "ERROR", "location": "do get_info", "log": str(e)})
elif do == 'request':
    try:
        result = Request(sys.argv[2],sys.argv[3])
        print(result)
    except Exception as e:
        print({"status": "ERROR", "location": "do request", "log": str(e)})
elif do == 'data_transform':
    try:
        arg = sys.argv
        result = DataTransform_IPTABLE(arg[2],arg[3],arg[4],arg[5],arg[6])
        print(result)
    except Exception as e:
        print({"status": "ERROR", "location": "do data_transform", "log": str(e)})
elif do == 'create_iptable':
    try:
        result = CreateIPTable(sys.argv[2],sys.argv[3])
        print(result)
    except Exception as e:
        print({"status": "ERROR", "location": "do create_table", "log": str(e)})
elif do == 'get_data':
    pass
