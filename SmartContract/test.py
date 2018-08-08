import IPControl

a = IPControl.IPControl("140.92.143.82","0xa790753b84164d4fd0ad4f85ac0f44760c3a4a99")

#print(a.GetSchema())    # Get the scheam in contract
#a.CreateTable("people")    # create local foreign table by contract fhash
#a.CommitShard("people")    # commit local fhash to contract
#print(a.GetInfo())    # Get info of contract fhash
#a.PushShard(2,"nice data of student ages.")    # be a saler


### Sale / Buy data
#Saler = a.GetSaleList()
#print(Saler)
#print(a.GetShardInfo(Saler[0]))

#a.Buy(Saler[0])


### Use data
Pocket = a.ShowPocket()
#print(Pocket)
#print(a.GetPocketShardInfo(Pocket[0]))

a.CreateTable("newPerson",Pocket[0])
