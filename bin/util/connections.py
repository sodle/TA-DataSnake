realm_name = 'TA-DataSnake-Connection'


class ConnectionManager(object):
    def __init__(self, service):
        self.service = service

    def list(self):
        for cred in self.service.storage_passwords:
            if cred.realm == realm_name:
                yield cred

    def get(self, name):
        for cred in self.list():
            if cred.username == name:
                return cred
