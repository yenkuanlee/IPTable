# -*- coding: UTF-8 -*-
import json
import ipfsapi
import IOTATransaction
import time
a = IOTATransaction.IOTATransaction()
Ftag = 'IPTABLETEST'
api = ipfsapi.connect('127.0.0.1', 5001)

To = 'BXOM9LUNLPSEXBRJV9UUNLHSUHABEOGHQOGNBNBUEYSGOFZOEPYKEYRSFTXBOEJLUODUQXXGQ9NWQBSGH'
TargerPeerID = 'KEVIN'

table_info = dict()
table_info['table_name'] = 'accounting'
table_info['table_schema'] = '(TSID bigint,Adate text,item text,description text,twd int)'
table_info['description'] = '這是Kevin的記帳'
table_info['fhash'] = a.GetFhash('accounting')
table_info['table_rowCount'] = 12#len(api.object_get(table_info['fhash'])['Links'])

pt = a.MakePreparingTransaction(To, json.dumps(table_info), tag=Ftag)
a.SendTransaction([pt])
print(a.GetTransactionHash())

#TID = 'GLKGBQOOHIUAJIYEPAWFNRTVYZIMIQYIUNPRNLSSJZTTIRSQVMARYQFJPESXXGHMYWBWHFITRQCAA9999'
#print(a.CreateTable('kevin',TID))
