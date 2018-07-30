from . import ForeignDataWrapper
import json

class IPFSFdw(ForeignDataWrapper):
    def __init__(self, fdw_options, fdw_columns):
        super(IPFSFdw, self).__init__(fdw_options, fdw_columns)
        self.fhash = fdw_options["fhash"]
        self.columns = fdw_columns

    def execute(self, quals, columns):
        import ipfsapi
        api = ipfsapi.connect('127.0.0.1', 5001)
        res = api.cat(self.fhash)
        Jres = json.loads(res)
        for line in Jres:
            line = dict((k.lower(), v) for k, v in line.iteritems())
            ltmp = list()
            for x in self.columns:
                ltmp.append(line[x])
            yield ltmp[:len(self.columns)]
