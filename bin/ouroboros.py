from splunklib.searchcommands import Configuration, GeneratingCommand, Option, dispatch
import sys
import json
import subprocess
from util import ConnectionManager


@Configuration(type='reporting')
class Ouroboros(GeneratingCommand):
    connection = Option(require=True)
    query = Option(require=True)

    def generate(self):
        connections = ConnectionManager(self.service)
        connection_string = connections.get(self.connection)

        if connection_string is None:
            raise KeyError('No such connection - {}'.format(self.connection))

        ds_proc = subprocess.Popen(['datasnake', connection_string.clear_password, self.query,
                                    '--output-format=json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ds_out, ds_err = ds_proc.communicate()
        for line in ds_out.split('\n'):
            if line.startswith('ROW'):
                _, _, db_row = line.split('\t')
                yield json.loads(db_row)
        if len(ds_err) > 0:
            raise RuntimeError(ds_err)


dispatch(Ouroboros, sys.argv, sys.stdin, sys.stdout, __name__)
