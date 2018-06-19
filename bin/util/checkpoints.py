import splunklib

realm_name = 'TA-DataSnake-Checkpoint'


class CheckpointManager(object):
    def __init__(self, service):
        # type: (splunklib.service) -> None
        self.service = service

    def list(self):
        for cred in self.service.storage_passwords:
            if cred.realm == realm_name:
                yield cred

    def get(self, name):
        for cred in self.list():
            if cred.username == name:
                return cred

    def create(self, name, value):
        self.service.storage_passwords.create(value, name, realm_name)

    def delete(self, name):
        self.service.storage_passwords.delete(name, realm_name)

    def update(self, name, value):
        self.delete(name)
        self.create(name, value)
