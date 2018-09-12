import ObjectNode
import json

table = ObjectNode.ObjectNode()
table.new("Student")

a = ObjectNode.ObjectNode()
a.new("Kevin")
a.AddField("Name","Kevin")
a.AddField("school","NCKU")
a.AddField("age","27")
a.AddField("StudentID","F74982260")

b = ObjectNode.ObjectNode()
b.new("John")
b.AddField("Name","John")
b.AddField("school","NTU")
b.AddField("age","29")
b.AddField("StudentID","23307")

c = ObjectNode.ObjectNode()
c.new("Mary")
c.AddRow({"school":"NCKU", "age":"25", "StudentID":"9527", "Name":"Mary"})

table.AddHash("1",a.ObjectHash)
table.AddHash("2",b.ObjectHash)
table.AddHash("3",c.ObjectHash)

print(table.ObjectHash)
