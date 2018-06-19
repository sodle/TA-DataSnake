from splunklib.searchcommands import Configuration, GeneratingCommand, Option, dispatch
import sys
import json
import subprocess


@Configuration(type='reporting')
class VersionCheck(GeneratingCommand):
    def generate(self):
        ds_proc = subprocess.Popen(['datasnake', '--env'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ds_out, ds_err = ds_proc.communicate()
        yield json.loads(ds_out)
        for line in ds_err.split('\n'):
            self.logger.error(line)


dispatch(VersionCheck, sys.argv, sys.stdin, sys.stdout, __name__)
