# IPTable

IPTable is a Decentralized DB table, which is implement by IPFS FDW.
Users can use the foreign table in sql language(including SELECT/INSERT/DELETE/UPDATE).
There are a hash bind with IPTable, called fhash.
By transmit the fhash to others node with same IPFS domain, people can get and use the IPTable immediatly.

In this project, there is a Ethereum smart contract to apply IPTable.
Users can deploy a contract with table schema, and people can use the contract to do cooperative operation with IPTable.
Through the smart contract, we can do the following things:
  - Create local foreign table by the schema in contract
  - Edit the foreign table
  - Commit fhash to the contract
  - Push table shard with some information and become a table saler
  - Look the information of table shard which had already be push
  - Buy some interesting table shard and put into pocket of contract
  - Create local foreign table which is received from pocket


## Install IPTable by Docker

Strongly suggest using docker to install IPTable now.

Unfortunately, not for mac!!!
  - https://github.com/docker/for-mac/issues/68

```
$ sudo docker build -t "iptable:test" .
$ sudo docker run -dti --network=host iptable:test /bin/sh
$ sudo docker exec -ti $CONTAINER_ID bash
$ cd ~/IPTable
$ git pull
$ sh deploy.sh
```


## Set up and test (ipfs_csv, ipfs_json, ipfs_object)
```
$ vi /tmp/test.csv
Year,Make,Model,Length
1997,Ford,E350,2.34
2000,Mercury,Cougar,2.38

$ ipfs add /tmp/test.csv 

$ sudo -u postgres psql

    CREATE EXTENSION multicorn;
    
    CREATE SERVER ipfs_srv foreign data wrapper multicorn options (
        wrapper 'multicorn.ipfs_csvfdw.IPFSFdw'
    );

    create foreign table ipfstest (
           year numeric,
           make character varying,
           model character varying,
           length numeric
    ) server ipfs_srv options (
           fhash 'QmbYMevyNwnHJNcF6qGpg3w7doSQW96JEnZghpeAxJsPBB',
           skip_header '1',
           delimiter ',');

    select * from ipfstest;

==========================================================================
$ vi /tmp/test.json
[{"Make": "Ford", "Length": 2.34, "Model": "E350", "Year": 1997}, {"Make": "Mercury", "Length": 2.38, "Model": "Cougar", "Year": 2000}]

$ ipfs add /tmp/test.json

$ sudo -u postgres psql

    CREATE SERVER ipfs_srv2 foreign data wrapper multicorn options (
        wrapper 'multicorn.ipfs_jsonfdw.IPFSFdw'
    );

    create foreign table ipfstest2 (
           Year numeric,
           Make character varying,
           Model character varying,
           Length numeric
    ) server ipfs_srv2 options (
           fhash 'Qmc6JiUQ1yahNpgHkqEA1xBtmp4hb6i5Z4RpVgqPQCm6kg'
    );

    select * from ipfstest2;

==========================================================================
$ ipfs add -r ~/Multicorn

$ sudo -u postgres psql

    CREATE SERVER ipfs_srv3 foreign data wrapper multicorn options (
        wrapper 'multicorn.ipfs_objectfdw.IPFSFdw'
    );

    create foreign table ipfstest3 (
        data text,
        name text,
        hash text,
        size int
    ) server ipfs_srv3 options (
           fhash 'QmQQa3HUgDtXzwwBcdcwsSVPWWJ7PVWc8UmbADV1FhxB8n'
    );

    select * from ipfstest3;
```

## IPTable FDW
IPTable FDW is a foreign data wrapper which use IPFS object to represent a table in PostgreSQL. 
The structure of IPTable object is a three level merkle tree. 
  - Level 1 : table
  - Level 2 : row
  - Level 3 : field

In a IPTable merkle tree, node is object hash and edge is the value of object. 

In the first level, node is the fhash which can represent a IPTable and will be put into the option of foreign table.
In the second level, node represent object hash of one row , and edge is a timestamp ID.
In the third level, node represent object hash of filed name, and edge is correspond value of field.
 
In a IPTable merkle tree, there is only one node in level 1(root); 
The number of nodes in level 2 is rowCount; 
The number of nodes in level 2 is qual to the number of field.

### Push data to ipfs object
```
$ python push_data.py 
    QmW5pgzxDJ8ao2eqKrnVse2idsABDikf55FYx4BBDj25ga
```

### Set up FDW and create foreign table
```
$ sudo -u postgres psql

    CREATE SERVER ipserver foreign data wrapper multicorn options (
        wrapper 'multicorn.ipfs_tablefdw.IPFSFdw'
    );

    create foreign table student (
        TSID bigint,
        Name text,
        school text,
        age int,
        StudentID text
    ) server ipserver options (
          table_name 'student',
          fhash 'QmW5pgzxDJ8ao2eqKrnVse2idsABDikf55FYx4BBDj25ga'
    );

    select * from student;
    insert into student values(1,'Dog','MCU',38,'9487');
    update student set name = 'Cat' where school = 'MCU';
    delete from student where name = 'Cat';
```

### Modify fhash and update foreign table
After executing sql language and update IPTable, the fhash in look up table will be changed. 
We can do the following syntax to modify the fhash of IPTable, so that the status of IPTable is the newest. 
This is only a option to protect IPTable because the FDW is still quering lookup table to get fhash.

```
    ALTER FOREIGN TABLE student OPTIONS (SET fhash 'QmW5pgzxDJ8ao2eqKrnVse2idsABDikf55FYx4BBDj25ga');
```

### Get fhash from lookup table in DB
```
    SELECT * FROM _lookup WHERE table_name = 'student';
```

## Smart Contract
To use the smart contract of IPTable, we have to prepare a ethereum node. 
We can use IPDC ER project, the best project in the world, to build a wonderful envirement with ethereum private chain and a private cluster of IPFS. 

### Deploy the contract
There are three arguments in deploy_iptable_contract.py
  - host
  - account
  - password

```
$ python3 deploy_iptable_contract.py
```

### Use the contract
There are a command line tool called IPControl.py. 

Users can modify the test.py and apply the smart contract with IPTable.

```
$ vi test.py
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



$ python3 test.py
```
