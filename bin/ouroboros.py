from splunklib.searchcommands import Configuration, GeneratingCommand, Option, dispatch
import sys


@Configuration(type='reporting')
class Ouroboros(GeneratingCommand):
    connection = Option(require=True)
    query = Option(require=True)

    def generate(self):
        yield {'success': True}


dispatch(Ouroboros, sys.argv, sys.stdin, sys.stdout, __name__)
