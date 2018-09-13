# -*- coding: UTF-8 -*-
import ipfsapi
import IOTATransaction
import json
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

def Publish(data_format, channel_tag, table_schema, table_rowCount, description, deadline):
    data_info = dict()
    data_info['data_format'] = data_format
    data_info['table_schema'] = table_schema
    data_info['table_rowCount'] = table_rowCount
    data_info['description'] = description
    data_info['deadline'] = deadline
    iotalent = IOTATransaction.IOTATransaction()
    try:
        pt = iotalent.MakePreparingTransaction(DontCareAddress, json.dumps(data_info), tag=channel_tag)
        iotalent.SendTransaction([pt])
        return {"status": "SUCCESS", "TID": iotalent.GetTransactionHash()}
    except Exception as e:
        return {"status": "ERROR", "location": "Function Publish", "log": str(e)}
    
     

try:
    do = sys.argv[1]
except:
    do = None

if do == 'publish':
    try:
        #Publish(data_format, channel_tag, table_schema, table_rowCount, description, deadline)
        arg = sys.argv
        result = Publish(arg[2],arg[3],arg[4],arg[5],arg[6],arg[7])
        print(result)
    except Exception as e:
        print({"status": "ERROR", "location": "do publish", "log": str(e)})
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
