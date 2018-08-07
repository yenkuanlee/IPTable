import IPControl

a = IPControl.IPControl("140.92.143.82","0xa790753b84164d4fd0ad4f85ac0f44760c3a4a99")
#print(a.GetSchema())
#print(a.GetInfo())
print(a.GetShardInfo("0xa790753b84164d4fd0ad4f85ac0f44760c3a4a99"))
#a.CreateTable()
#a.CommitShard("888")
#a.PushShard(2,"Kevin")
#a.UploadFhash("test")
