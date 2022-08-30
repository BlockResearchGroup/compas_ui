"""
********************************************************************************
session
********************************************************************************

.. currentmodule:: compas_ui.session


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Session

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import atexit

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
    """The session singleton tracks data stored in an app.

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
    filename : str
        Name of the session file used for persistent storage.
    filepath : str
        Full path to the session file used for persistent storage.

    """

    def __init__(self, name=None, directory=None, extension="json", autosave=False):
        self._history = []
        self._current = -1
        self.data = {}
        self.directory = directory or os.path.realpath(sys.path[0])
        self.name = name or self.__class__.__name__
        self.extension = extension
        self.autosave = autosave
        # self.record()

    def __str__(self):
        return json_dumps(self.data, pretty=True)

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
        return "{}.{}".format(self.name, self.extension)

    @property
    def filepath(self):
        return os.path.join(self.directory, self.filename)

    @filepath.setter
    def filepath(self, filepath):
        dirname, basename = os.path.split(filepath)
        filename, extension = os.path.splitext(basename)
        extension = extension.replace(".", "")
        self.directory = dirname
        self.name = filename
        self.extension = extension

    @property
    def history(self):
        return self._history

    def reset(self):
        """Reset the session to a blank state.

        Returns
        -------
        None

        """
        self._history = []
        self._current = -1
        self.data = {}
        # self.record()

    def record(self):
        """Add the current data to recorded history making it available for undo/redo.

        Returns
        -------
        None

        """
        if self._current > -1:
            if self._current < len(self._history) - 1:
                # remove everything that comes after current
                # but keep current
                self._history[:] = self._history[: self._current + 1]

        self._history.append(json_dumps(self.data))
        self._current = len(self._history) - 1

    def undo(self):
        """Undo recent changes by reverting the data to the version recorded before the current one.

        Returns
        -------
        None

        """
        if self._current < 0:
            print("Nothing to undo!")
            return

        if self._current == 0:
            print("Nothing more to undo!")
            return

        self._current -= 1
        self.data = json_loads(self._history[self._current])

    def redo(self):
        """Redo recent changes by reverting the data to the version recorded after the current one.

        Returns
        -------
        None

        """
        if self._current < 0:
            print("Nothing to redo!")
            return

        if self._current == len(self._history) - 1:
            print("Nothing more to redo!")
            return

        self._current += 1
        self.data = json_loads(self._history[self._current])

    def save(self):
        """Save the session data to the current file.

        Returns
        -------
        None

        """
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
