import splunklib.client

realm_name = 'TA-DataSnake-Connection'


class ConnectionManager(object):
    def __init__(self, service):
        # type: (splunklib.service) -> None
        self.service = splunklib.client.connect(token=service.token, autologin=True)

    def list(self):
        for cred in self.service.storage_passwords:
            if cred.realm == realm_name:
                yield cred

    def get(self, name):
        for cred in self.list():
            if cred.username == name:
                return cred
