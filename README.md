# IPTable

## Set up and test
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
        Name text,
        school text,
        age int,
        StudentID text
    ) server ipserver options (
          fhash 'QmW5pgzxDJ8ao2eqKrnVse2idsABDikf55FYx4BBDj25ga'
    );

    select * from student;
```

### modify fhash and update table

```
    ALTER FOREIGN TABLE student OPTIONS (SET fhash 'QmW5pgzxDJ8ao2eqKrnVse2idsABDikf55FYx4BBDj25ga');
```
