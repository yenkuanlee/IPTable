# IPTable

```
$ sudo /etc/init.d/postgresql start

$ ipfs init

$ ipfs daemon &

$ vi /tmp/test.csv
1997,Ford,E350,2.34
2000,Mercury,Cougar,2.38

$ ipfs add /tmp/test.csv 

$ sudo -u postgres psql

    CREATE EXTENSION multicorn;
    
    CREATE SERVER ipfs_srv foreign data wrapper multicorn options (
        wrapper 'multicorn.ipfsfdw.IPFSFdw'
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
```
