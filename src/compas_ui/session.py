from compas.data import json_load
from compas.data import json_dump
from compas.data import json_dumps


class Session(object):

    JSONSCHEMA = None

    _instance = None

    def __new__(cls, name, *args, **kwargs):
        if not cls._instance:
            self = super(Session, cls).__new__(cls)
            self.data = {}
            self.name = name
            cls._instance = self
        return cls._instance

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self):
        print(json_dumps(self.data, pretty=True))

    def load(self, filepath):
        self.data = json_load(filepath)

    def save(self, filepath):
        json_dump(self.data, filepath)

    def validate(self):
        # run json validation on data
        # using the JSONSCHEMA
        pass
