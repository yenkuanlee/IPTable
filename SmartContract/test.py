import IPControl

#a = IPControl.IPControl("140.92.143.82","0x4f01d4ea522dfc29ce8623c5d7564a80adcca2cc")
#a = IPControl.IPControl("140.92.143.82","0x85a203870a8f3b61bab23dc4c6d1c17cfa8ee59f")
###a = IPControl.IPControl("140.92.143.208","0xfd01ebea0ba1c522c3f4adf2cead4991f8c1a0d4")

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
#Pocket = a.ShowPocket()
#print(Pocket)
#print(a.GetPocketShardInfo(Pocket[0]))

#a.CreateTable("Person",Pocket[0])
