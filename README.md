# IPTable

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
```
