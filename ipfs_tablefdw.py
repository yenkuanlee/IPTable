from . import ForeignDataWrapper
import ipfsapi
import json
import ObjectNode
import time
from multiprocessing import Pool
import os
import psycopg2

class IPFSFdw(ForeignDataWrapper):
    def __init__(self, fdw_options, fdw_columns):
        super(IPFSFdw, self).__init__(fdw_options, fdw_columns)
        self.randomid = fdw_options["randomid"]
        CleanNode = ObjectNode.ObjectNode()
        CleanNode.new(self.randomid)
        self.fhash = fdw_options.get('fhash', CleanNode.ObjectHash)
        self.columns = fdw_columns
        
        self.tx_hook = fdw_options.get('tx_hook', False)
        self._row_id_column = fdw_options.get('row_id_column',
                                          list(self.columns.keys())[0])

        self.api = ipfsapi.connect('127.0.0.1', 5001)
        self.conn = psycopg2.connect(database="postgres",user="postgres",host="127.0.0.1", port="5432")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS _lookup(randomid text PRIMARY KEY, fhash text);")
        self.conn.commit()
        self.cur.execute("SELECT FHASH FROM _lookup WHERE randomid = '"+self.randomid+"';")
        try:
            DontCare = self.cur.fetchone()[0]
        except:
            self.cur.execute("INSERT INTO _lookup VALUES('"+self.randomid+"','"+self.fhash+"');")
            self.conn.commit()

    def execute(self, quals, columns):
        self.cur.execute("SELECT FHASH FROM _lookup WHERE randomid = '"+self.randomid+"';")
        self.fhash = self.cur.fetchone()[0]
        Jres = self.api.object_get(self.fhash)
        for x in Jres['Links']:
            a = ObjectNode.ObjectNode()
            a.load(x['Hash'])
            line = a.GetInfo()
            line = dict((k.lower(), v) for k, v in line.iteritems())
            ltmp = list()
            for x in self.columns:
                ltmp.append(line[x])
            yield ltmp[:len(self.columns)]

    def insert(self, values):
        table = ObjectNode.ObjectNode()
        table.load(self.fhash)
        a = ObjectNode.ObjectNode()
        a.new("dog")
        a.AddRow(values)
        Tlist = table.GetObjectInfo()["Links"]
        table.AddHash(str(len(Tlist)+1),a.ObjectHash)
        self.fhash = table.ObjectHash
        self.cur.execute("UPDATE _lookup SET fhash = '"+self.fhash+"' WHERE randomid = '"+self.randomid+"';")
        self.conn.commit()


    @property
    def rowid_column(self):
        return self._row_id_column

    def begin(self, serializable):
        if self.tx_hook:
            log_to_postgres('BEGIN')

    def sub_begin(self, level):
        if self.tx_hook:
            log_to_postgres('SUBBEGIN')

    def sub_rollback(self, level):
        if self.tx_hook:
            log_to_postgres('SUBROLLBACK')

    def sub_commit(self, level):
        if self.tx_hook:
            log_to_postgres('SUBCOMMIT')

    def commit(self):
        if self.tx_hook:
            log_to_postgres('COMMIT')

    def pre_commit(self):
        if self.tx_hook:
            log_to_postgres('PRECOMMIT')
