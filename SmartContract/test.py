import IPControl

a = IPControl.IPControl("140.92.143.82","0xa790753b84164d4fd0ad4f85ac0f44760c3a4a99")
#print(a.GetSchema())    # Get the scheam in contract
#a.CreateTable("people")    # create local foreign table by contract fhash
#a.UploadFhash("people")    # commit local fhash to contract
#print(a.GetInfo())    # Get info of contract fhash
#a.PushShard(2,"nice data of student ages.")    # be a saler
Saler = a.GetSaleList()
#print(a.GetSaleList())
print(a.GetShardInfo(Saler[0]))

