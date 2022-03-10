from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import atexit

from collections import deque

from compas.data import json_load
from compas.data import json_loads
from compas.data import json_dump
from compas.data import json_dumps

from compas_ui.singleton import Singleton


def autosave():
    """Automatically save the session to a file by registering this function with `atexit`."""
    session = Session()
    if session.autosave:
        session.save()


atexit.register(autosave)


class Session(Singleton):
    """The Session singleton that tracks states of an app.

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
        Defaults to 'json'.
    autosave : bool, optional
        If True, automatically save the session to file at interpreter shutdown.
        Defaults to False.

    Attributes
    ----------
    name : str
        Name of the session.
    directory : str
        The directory where the session should be saved.
    extension : str
        The extension used for saving the session to disk.
    autosave : bool
        If True, automatically save the session to file at interpreter shutdown.
    dataschema : schema.Schema
        The schema of the session data.
    historyschema : schema.Schema
        The schema of the session data history.
    filename : str
        Name of the session file used for persistent storage.
    filepath : str
        Full path to the session file used for persistent storage.

    """

    def __init__(self, name=None, directory=None, extension='json', autosave=False):
        self._history = deque()
        self._current = 0
        self.data = {}
        self.directory = directory or os.path.realpath(sys.path[0])
        self.name = name or self.__class__.__name__
        self.extension = extension
        self.autosave = autosave

    def __str__(self):
        return json_dumps(self.snapshot, pretty=True)

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
    def filename(self):
        return '{}.{}'.format(self.name, self.extension)

    @property
    def filepath(self):
        return os.path.join(self.directory, self.filename)

    @filepath.setter
    def filepath(self, filepath):
        dirname, basename = os.path.split(filepath)
        filename, extension = os.path.splitext(basename)
        extension = extension.replace('.', '')
        self.directory = dirname
        self.name = filename
        self.extension = extension

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
            print("Nothing more to redo!")
            return
        self._current -= 1
        self.data = json_loads(self._history[self._current])

    def save(self):
        """Save the session data to the current file.

        Returns
        -------
        None

        """
        # session = {'data': self.data, 'current': self._current, 'history': list(self._history)}
        json_dump(self.data, self.filepath)

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
        # session = {'data': self.data, 'current': self._current, 'history': list(self._history)}
        json_dump(self.data, filepath)

    def load(self, filepath=None):
        """Load session data from a session file.

        Parameters
        ----------
        filepath : str
            Path to an existing session file.

        Returns
        -------
        None

        """
        # session = json_load(filepath or self.filepath)
        # self._current = session['current']
        # self._history = deque(session['history'])
        # self.data = session['data']
        self.data = json_load(filepath or self.filepath)

    # def validate_data(self):
    #     """Validate the data against the data schema.

    #     Returns
    #     -------
    #     None

    #     """
    #     data = self.schema.validate(self.data)
    #     return data

    # def validate_history(self):
    #     """Validate the data history against the data history  schema.

    #     Returns
    #     -------
    #     None

    #     """
    #     pass
