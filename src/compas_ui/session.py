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
    session.save()


class Session(object):
    """Session singleton.

    Parameters
    ----------
    name : str, optional
        Name of the session.
        Defaults to the name of the session class.
    directory : str, optional
        The directory where the session should be saved.
        Defaults to the directory containing the script running the session.
    extension : str, optional
        The extension used for saving the session to disk.
    autosave : bool, optional
        If True, automatically save the session to file at interpreter shutdown.

    Attributes
    ----------
    dataschema : schema.Schema
        The schema of the session data.
    historyschema : schema.Schema
        The schema of the session data history.
    filename : str
        Name of the session file used for persistent storage.
    filepath : str
        Full path to the session file used for persistent storage.

    """

    _instance = None

    def __new__(cls, name=None, directory=None, extension='json', autosave=True):
        if not cls._instance:
            self = super(Session, cls).__new__(cls)
            self._history = deque()
            self._current = 0
            self.data = {}
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
    def dataschema(self):
        from schema import Schema
        return Schema(dict)

    @property
    def historyschema(self):
        raise NotImplementedError

    @property
    def filename(self):
        return '{}.{}'.format(self.name, self.extension)

    @property
    def filepath(self):
        return os.path.join(self.directory, self.filename)

    @property
    def history(self):
        return self._history

    def record(self):
        """Add the current data to recorded history making it available for undo/redo.

        Returns
        -------
        None

        """
        if self._current != 0:
            self._history = deque(list(self._history)[self._current + 1:])
        self._history.appendleft(json_dumps(self.data))

    def undo(self):
        """Undo recent changes by reverting the data to the version recorded before the current one.

        Returns
        -------
        None

        """
        if self._current == len(self._history) - 1:
            print("Nothing more to undo!")
            return
        self._current += 1
        self.data = json_loads(self._history[self._current])

    def redo(self):
        """Redo recent changes by reverting the data to the version recorded after the current one.

        Returns
        -------
        None

        """
        if self._current == 0:
            return
        self._current -= 1
        self.data = json_loads(self._history[self._current])

    def save(self):
        """Save the session data to the current file.

        Returns
        -------
        None

        """
        session = {'data': self.data, 'history': list(self._history)}
        json_dump(session, self.filepath)

    def saveas(self, filepath):
        """Save the session to a new file.

        Parameters
        ----------
        filepath : str
            Path to a file for saving the session data.

        Returns
        -------
        None

        """
        session = {'data': self.data, 'history': list(self._history)}
        json_dump(session, filepath)

    def load(self, filepath):
        """Load session data from a session file.

        Parameters
        ----------
        filepath : str
            Path to an existing session file.

        Returns
        -------
        None

        """
        session = json_load(filepath)
        self.data = session['data']
        self._history = deque(session['history'])

    def validate_data(self):
        """Validate the data against the data schema.

        Returns
        -------
        None

        """
        data = self.schema.validate(self.data)
        return data

    def validate_history(self):
        """Validate the data history against the data history  schema.

        Returns
        -------
        None

        """
        pass


atexit.register(autosave)
