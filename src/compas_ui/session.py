import sys
import os
import atexit

from collections import deque

from compas.data import json_load
from compas.data import json_loads
from compas.data import json_dump
from compas.data import json_dumps


def autosave():
    """Automatically save the session to a file by registering this function with `atexit`."""
    session = Session()
    session.store()


class Session(object):
    """Session singleton.
    
    Parameters
    ----------
    name : str, optional
        Name of the session.
        Defaults to the name of the session class.
    extension : str, optional
        The extension used for saving the session to disk.
    directory : str, optional
        The directory where the session should be saved.
        Defaults to the directory containing the script running the session.
    depth : int, optional
        The number of changes in the session data to keep track of.
        As in the "depth" of the session history...
    autosave : bool, optional
        If True, automatically save the session to file at interpreter shutdown.
    
    """

    _instance = None

    def __new__(cls, name=None, directory=None, extension='json', depth=10, autosave=True):
        if not cls._instance:
            self = super(Session, cls).__new__(cls)
            self.data = {}
            self.history = deque()
            self.depth = depth
            self.directory = directory or os.path.realpath(sys.path[0])
            self.name = name or self.__class__.__name__
            self.extension = extension
            self.autosave = autosave
            cls._instance = self
        return cls._instance

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self):
        print(json_dumps(self.data, pretty=True))

    def __del__(self):
        # automatically save the session to file
        # when a script ends or the context is deleted
        # json_dump(self.data, self.filepath)
        # apparently this is not a good idea
        # https://stackoverflow.com/questions/23422188/why-am-i-getting-nameerror-global-name-open-is-not-defined-in-del/29737870
        pass
    
    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    @property
    def schema(self):
        from schema import Schema
        return Schema({
            'data': dict,
            'history': [str]
        })

    @property
    def basename(self):
        return '{}.{}'.format(self.name, self.extension)

    @property
    def filepath(self):
        return os.path.join(self.directory, self.basename)

    def record(self):
        while len(self.history) > self.depth:
            data = self.history.popleft()
            del data
        self.history.append(json_dumps(self.data))

    def back(self):
        self.data = json_loads(self.history.pop())

    def forward(self):
        self.data = json_loads(self.history.pop())

    def save(self, filepath=None):
        filepath = filepath or self.filepath
        session = {'data': self.data, 'history': list(self.history)}
        json_dump(session, filepath)

    def load(self, filepath):
        session = json_load(filepath)
        self.data = session['data']
        self.history = deque(session['history'])

    def loads(self, s):
        pass

    def validate(self):
        session = self.schema.validate({'data': self.data, 'history': list(self.history)})
        return session


atexit.register(autosave)
