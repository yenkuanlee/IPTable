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
        self.Dflag = False
        self.Dlist = list()
        self.randomid = fdw_options["randomid"]
        CleanNode = ObjectNode.ObjectNode()
        CleanNode.new(self.randomid)
        self.fhash = fdw_options.get('fhash', CleanNode.ObjectHash)
        self.columns = fdw_columns
        self.tx_hook = fdw_options.get('tx_hook', False)
        self._row_id_column = fdw_options.get('row_id_column',list(self.columns.keys())[0])
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
            line['tsid'] = x['Name']
            ltmp = list()
            for y in self.columns:
                ltmp.append(line[y])
            yield ltmp[:len(self.columns)]
        # For Delete
        if self.Dflag:
            table = ObjectNode.ObjectNode()
            table.load(self.fhash)
            for x in self.Dlist:
                table.RemoveHash(x)
            self.fhash = table.ObjectHash
            self.cur.execute("UPDATE _lookup SET fhash = '"+self.fhash+"' WHERE randomid = '"+self.randomid+"';")
            self.conn.commit()
            self.Dlist = list()
            self.Dflag = False

    def insert(self, values):
        table = ObjectNode.ObjectNode()
        table.load(self.fhash)
        a = ObjectNode.ObjectNode()
        a.new("dog")
        a.AddRow(values)
        Tlist = table.GetObjectInfo()["Links"]
        ts = str(int(time.time()*1000))
        table.AddHash(ts,a.ObjectHash)
        self.fhash = table.ObjectHash
        self.cur.execute("UPDATE _lookup SET fhash = '"+self.fhash+"' WHERE randomid = '"+self.randomid+"';")
        self.conn.commit()
        self.Dflag = False

    def delete(self, oldvalues):
        self.Dlist.append(oldvalues)


    @property
    def rowid_column(self):
        self.Dflag = True
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
