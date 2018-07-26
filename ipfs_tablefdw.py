from . import ForeignDataWrapper
import ipfsapi
import json
import ObjectNode

class IPFSFdw(ForeignDataWrapper):
    def __init__(self, fdw_options, fdw_columns):
        super(IPFSFdw, self).__init__(fdw_options, fdw_columns)
        self.fhash = fdw_options["fhash"]
        self.columns = fdw_columns
        
        self.tx_hook = fdw_options.get('tx_hook', False)
        self._row_id_column = fdw_options.get('row_id_column',
                                          list(self.columns.keys())[0])

        self.api = ipfsapi.connect('127.0.0.1', 5001)

    def execute(self, quals, columns):
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
        table.AddHash("4",a.ObjectHash)
        exit(table.ObjectHash)



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
