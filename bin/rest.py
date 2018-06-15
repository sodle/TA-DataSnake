import subprocess
import json
from splunk.rest import BaseRestHandler


class VersionCheck(BaseRestHandler):
    def __init__(self, method, request_info, response_info, session_key):
        BaseRestHandler.__init__(self, method, request_info, response_info, session_key)
        self.response.setHeader('content-type', 'application/json')

    def handle_VIEW(self):
        self.handle_GET()

    def handle_GET(self):
        try:
            datasnake_proc = subprocess.Popen(['datasnake', '--env'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = datasnake_proc.communicate()
            self.response.write(out)
        except OSError as e:
            self.response.write(json.dumps({'DataSnake Core': 'Not Installed', 'ex': e.strerror}))
