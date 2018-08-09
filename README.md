# IPTable

IPTable is a Decentralized DB table, which is implement by IPFS FDW.
Users can use the foreign table in sql language(including SELECT/INSERT/DELETE/UPDATE).
There are a hash bind with IPTable, called fhash.
By transmit the fhash to others node with same IPFS domain, people can get and use the IPTable immediatly.

In this project, there is a Ethereum smart contract to apply IPTable.
Users can deploy a contract with table schema, and people can use the contract to do cooperative operation with IPTable.
Through the smart contract, we can do the following things:
  - create local foreign table by the schema in contract
  - edit the foreign table
  - commit fhash to the contract
  - push table shard with some information and become a table saler
  - look the information of table shard which had already be push
  - buy some interesting table shard and put into pocket of contract
  - create local foreign table which is received from pocket


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



## Set up and test (ipfs_csv, ipfs_json, ipfs_object)
```
$ sudo /etc/init.d/postgresql start

$ ipfs init

$ ipfs daemon &

==========================================================================
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

```
    ALTER FOREIGN TABLE student OPTIONS (SET fhash 'QmW5pgzxDJ8ao2eqKrnVse2idsABDikf55FYx4BBDj25ga');
```

### Get fhash from lookup table in DB
```
    SELECT * FROM _lookup WHERE table_name = 'student';
```
