from splunklib.searchcommands import Configuration, GeneratingCommand, Option, dispatch
import sys
import json
import subprocess


@Configuration(type='reporting')
class Ouroboros(GeneratingCommand):
    connection = Option(require=True)
    query = Option(require=True)

    def generate(self):
        ds_proc = subprocess.Popen(['datasnake', self.connection, self.query,
                                    '--output-format=json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ds_out, ds_err = ds_proc.communicate()
        for line in ds_out.split('\n'):
            if line.startswith('ROW'):
                _, _, db_row = line.split('\t')
                yield json.loads(db_row)
        for line in ds_err.split('\n'):
            self.logger.error(line)


dispatch(Ouroboros, sys.argv, sys.stdin, sys.stdout, __name__)
