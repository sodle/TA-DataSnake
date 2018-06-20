from splunklib.modularinput import Script, Scheme, Argument, Event
import subprocess
import sys
from util import ConnectionManager, CheckpointManager


class DataSnakeTailModularInput(Script):
    def get_scheme(self):
        scheme = Scheme('DataSnake Tailing Modular Input')
        scheme.description = 'Follow the results of a database query by a rising timestamp column.'
        scheme.add_argument(Argument('connection', title='Connection',
                                     description='Connection name as defined in DataSnake setup',
                                     data_type=Argument.data_type_string, required_on_create=True))
        scheme.add_argument(Argument('query', title='Query', data_type=Argument.data_type_string,
                                     required_on_create=True))
        scheme.add_argument(Argument('timestamp_column', title='Timestamp Column',
                                     description='Column name used for populating event timestamp and checkpoints',
                                     data_type=Argument.data_type_string, required_on_create=True))
        scheme.add_argument(Argument('format', title='Format', description='Format of rows (JSON or classic DBX)',
                                     data_type=Argument.data_type_string,
                                     validation='format = "dbx" OR format = "json"',  required_on_create=True)),
        return scheme

    def stream_events(self, inputs, ew):
        for name, item in inputs.inputs.iteritems():
            conn_man = ConnectionManager(self.service)
            conn = conn_man.get(item['connection']).clear_password
            query = item['query']
            fmt = item['format']
            ts_col = item['timestamp_column']
            check_man = CheckpointManager(self.service)
            check = check_man.get(name)
            ds_args = ['datasnake', conn, query, '--output-format={}'.format(fmt), '--index={}'.format(ts_col)]
            if check is not None:
                ds_args.append('--offset={}'.format(check.clear_password))
            ds_proc = subprocess.Popen(ds_args)
            ds_out, ds_err = ds_proc.communicate()
            for line in ds_out.split('\n'):
                if line.startswith('ROW'):
                    _, _, row = line.split('\t')
                    ew.write_event(Event(data=row, stanza=name, source=name, sourcetype='datasnake:{}'.format(fmt)))
                if line.startswith('CHECKPOINT'):
                    _, checkpoint = line.split('\t')
                    if check is None:
                        check_man.create(name, checkpoint)
                    else:
                        check_man.update(name, checkpoint)
            for line in ds_err.split('\n'):
                ew.log('ERROR', 'DataSnake error: {}'.format(line))


if __name__ == '__main__':
    sys.exit(DataSnakeTailModularInput().run(sys.argv))
