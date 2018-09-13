# -*- coding: UTF-8 -*-
import ipfsapi
import IOTATransaction
import json
import requests
import sys
import time

'''
A publish
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

def Publish(data_format, channel_tag, table_schema, table_rowCount, description, deadline, wallet_address):
    data_info = dict()
    data_info['data_format'] = data_format
    data_info['table_schema'] = table_schema
    data_info['table_rowCount'] = table_rowCount
    data_info['description'] = description
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
    
     

try:
    do = sys.argv[1]
except:
    do = None

if do == 'publish':
    try:
        arg = sys.argv
        result = Publish(arg[2],arg[3],arg[4],arg[5],arg[6],arg[7],arg[8])
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
    pass
elif do == 'data_transform':
    pass
elif do == 'create_table':
    pass
elif do == 'get_data':
    pass

To = 'BXOM9LUNLPSEXBRJV9UUNLHSUHABEOGHQOGNBNBUEYSGOFZOEPYKEYRSFTXBOEJLUODUQXXGQ9NWQBSGH'
TargerPeerID = 'KEVIN'

table_info = dict()
table_info['table_name'] = 'accounting'
table_info['table_schema'] = '(TSID bigint,Adate text,item text,description text,twd int)'
table_info['description'] = '這是Kevin的記帳'
table_info['fhash'] = a.GetFhash('accounting')
table_info['table_rowCount'] = 12#len(api.object_get(table_info['fhash'])['Links'])

#pt = a.MakePreparingTransaction(To, json.dumps(table_info), tag=Ftag)
#a.SendTransaction([pt])
#print(a.GetTransactionHash())

#TID = 'GLKGBQOOHIUAJIYEPAWFNRTVYZIMIQYIUNPRNLSSJZTTIRSQVMARYQFJPESXXGHMYWBWHFITRQCAA9999'
#print(a.CreateTable('kevin',TID))
