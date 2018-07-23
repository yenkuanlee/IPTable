from . import ForeignDataWrapper
import time

class IPFSFdw(ForeignDataWrapper):
    def __init__(self, fdw_options, fdw_columns):
        super(IPFSFdw, self).__init__(fdw_options, fdw_columns)
        self.fhash = fdw_options["fhash"]
        self.delimiter = fdw_options.get("delimiter", ",")
        self.quotechar = fdw_options.get("quotechar", '"')
        self.skip_header = int(fdw_options.get('skip_header', 0))
        self.columns = fdw_columns

    def execute(self, quals, columns):
        import ipfsapi
        api = ipfsapi.connect('127.0.0.1', 5001)
        res = api.cat(self.fhash)
        dlist = res.split("\n")
        cnt = 0
        for line in dlist:
            if line=="":continue
            tmp = line.split(self.delimiter)
            if len(tmp) > len(self.columns):
               #log_to_postgres("data format error")
               exit("data format error")
            if cnt >= self.skip_header:
                yield tmp[:len(self.columns)]
            cnt += 1
