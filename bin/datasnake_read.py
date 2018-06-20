from splunklib.modularinput import Script, Scheme, Argument, Event
import subprocess
import sys
from util import ConnectionManager


class DataSnakeReadModularInput(Script):
    def get_scheme(self):
        scheme = Scheme('DataSnake Reader Modular Input')
        scheme.description = 'Index the results of a database query in their entirety.'
        scheme.add_argument(Argument('connection', title='Connection',
                                     description='Connection name as defined in DataSnake setup',
                                     data_type=Argument.data_type_string, required_on_create=True))
        scheme.add_argument(Argument('query', title='Query', data_type=Argument.data_type_string,
                                     required_on_create=True))
        scheme.add_argument(Argument('format', title='Format', description='Format of rows (JSON or classic DBX)',
                                     data_type=Argument.data_type_string,
                                     validation='format = "dbx" OR format = "json"',  required_on_create=True))
        return scheme

    def stream_events(self, inputs, ew):
        for name, item in inputs.inputs.iteritems():
            conn_man = ConnectionManager(self.service)
            conn = conn_man.get(item['connection']).clear_password
            query = item['query']
            fmt = item['format']
            ds_proc = subprocess.Popen(['datasnake', conn, query, '--output-format={}'.format(fmt)],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ds_out, ds_err = ds_proc.communicate()
            for line in ds_out.split('\n'):
                if line.startswith('ROW'):
                    _, _, row = line.split('\t')
                    ew.write_event(Event(data=row, stanza=name, source=name, sourcetype='datasnake:{}'.format(fmt)))
            for line in ds_err.split('\n'):
                if len(line) > 0:
                    ew.log('ERROR', 'DataSnake error: {}'.format(line))


if __name__ == '__main__':
    sys.exit(DataSnakeReadModularInput().run(sys.argv))
