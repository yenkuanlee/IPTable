import IPControl

a = IPControl.IPControl("140.92.143.82","0xa790753b84164d4fd0ad4f85ac0f44760c3a4a99")
print(a.GetInfo())

a.CreateTable()

#a.SetShard("888")
