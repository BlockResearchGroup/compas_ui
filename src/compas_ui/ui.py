"""
********************************************************************************
ui
********************************************************************************

.. currentmodule:: compas_ui.ui


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    UI

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from subprocess import Popen
from subprocess import PIPE
import tempfile

import compas
import compas_rhino

from compas.utilities import timestamp
from compas.plugins import pluggable

from compas_cloud import Proxy

from compas_ui.singleton import Singleton
from compas_ui.session import Session
from compas_ui.scene import Scene
from compas_ui.controller import Controller

try:
    from compas_ui.rhino.forms import CondaEnvsForm
    from compas_ui.rhino.forms import FileForm
    from compas_ui.rhino.forms import FolderForm
    from compas_ui.rhino.forms import SceneObjectsForm
    from compas_ui.rhino.forms import SearchPathsForm
except ImportError:
    pass


@pluggable(category="ui", selector="collect_all")
def register(ui):
    pass


@pluggable(category="ui", selector="collect_all")
def pre_undo(ui):
    pass


@pluggable(category="ui", selector="collect_all")
def post_undo(ui):
    pass


@pluggable(category="ui", selector="collect_all")
def pre_redo(ui):
    pass


@pluggable(category="ui", selector="collect_all")
def post_redo(ui):
    pass


class UI(Singleton):
    """UI singleton.

    Attributes
    ----------
    name : str
        The name of the app.
    scene : :class:`compas_ui.scene.Scene`
        The compas_ui scene object.
    proxy : :class:`compas_cloud.Proxy`
        The compas_cloud Proxy object to communicate with a compas_cloud server.
    session : :class:`compas_ui.session.Session`
        The compas_ui session object.
    settings : dict[str, Any]
        A configuration dict for the app.

    """

    def __init__(self):
        config = {"settings": {"cloud": {"background": True}}}

        self._current = -1
        self._depth = 53
        self._history = []
        self._tempdir = tempfile.gettempdir()
        self._controller_class = Controller

        self.registry = {}
        self.config = config
        self.settings = self.config["settings"] or {}

        self.name = "COMPAS"
        self.condadir = None
        self.dirname = None
        self.basename = "{}.ui".format(self.name)

        self.session = Session(name=self.name)
        self.scene = Scene()
        self.controller = self._controller_class(self)
        self.proxy = None

        register(self)
        self.cloud_start()

    @property
    def state(self):
        state = {}
        state["session"] = self.session.data
        state["scene"] = self.scene.state
        state["settings"] = self.settings
        return state

    @state.setter
    def state(self, state):
        self.session.data = state["session"]
        self.scene.state = state["scene"]
        self.settings = state["settings"]

    # ========================================================================
    # Init
    # ========================================================================

    @staticmethod
    def reset():
        UI._instances = {}

    def restart(self):
        self.session.reset()
        self.scene.clear()
        self.cloud_restart()

    # ========================================================================
    # Info
    # ========================================================================

    @staticmethod
    def error(*args, **kwargs):
        """Decorator for functions that require proper error handling.

        Parameters
        ----------
        *args : list
            ???
        **kwargs : dict
            ???

        Returns
        -------
        callable

        """
        from .rhino.forms import error

        return error(*args, **kwargs)

    # ========================================================================
    # Cloud
    # ========================================================================

    def cloud_start(self):
        """Start the command server.

        Returns
        -------
        None

        """
        settings = self.settings.get("cloud") or {}
        self.proxy = Proxy(**settings)

    def cloud_restart(self):
        """Restart the command server.

        Returns
        -------
        None

        """
        if self.proxy:
            self.proxy.restart()
        else:
            self.cloud_start()

    def cloud_shutdown(self):
        """Shut down the command server.

        Returns
        -------
        None

        """
        if self.proxy:
            self.proxy.shutdown()

    # ========================================================================
    # Environments
    # ========================================================================

    def conda_envs(self):
        """Display a list of available conda environments.

        Returns
        -------
        None

        """
        if not self.condadir:
            folder = FolderForm.select()
            if not folder:
                return
            self.condadir = folder

        # replace with conda object
        conda = os.path.join(self.condadir, "condabin", "conda")
        process = Popen(["{} info --envs".format(conda)], stdout=PIPE, shell=True)
        out = process.stdout.read().decode()
        lines = out.split("\n")

        envs = []
        for line in lines:
            if line.startswith("#"):
                continue
            parts = line.strip().split()
            if parts and len(parts) > 1:
                envs.append((parts[0], parts[-1]))

        form = CondaEnvsForm(envs)
        form.show()

    def rhinopython_searchpaths(self):
        """Modify the Rhino Python search paths.

        Returns
        -------
        None

        """
        dialog = SearchPathsForm()
        dialog.show()

    # ========================================================================
    # Scene
    # ========================================================================

    def scene_clear(self):
        """Clear all objects from the scene.

        Returns
        -------
        None

        """
        self.scene.clear()
        self.record()

    def scene_update(self):
        """Update the scene.

        Returns
        -------
        None

        """
        self.scene.update()
        self.record()

    def scene_objects(self):
        """Display a form with all objects in the scene.

        Returns
        -------
        None

        """
        form = SceneObjectsForm(self.scene)
        if form.show():
            self.scene.update()
            self.record()

    # ========================================================================
    # State
    # ========================================================================

    def record(self, eventname=None):
        """Record the current state of the UI.

        Returns
        -------
        None

        """
        if self._current > -1:
            if self._current < len(self._history) - 1:
                self._history[:] = self._history[: self._current + 1]

        filename = "COMPAS_UI.history.{}".format(timestamp())
        filepath = os.path.join(self._tempdir, filename)

        compas.json_dump(self.state, filepath)
        self._history.append((filename, eventname))

        h = len(self._history)
        if h > self._depth:
            self._history[:] = self._history[h - self._depth :]
        self._current = len(self._history) - 1

    def undo(self):
        """Undo changes in the UI by rewinding to a recorded state.

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
        filename, _ = self._history[self._current]
        filepath = os.path.join(self._tempdir, filename)

        self.scene.clear()
        pre_undo(self)
        self.state = compas.json_load(filepath)
        post_undo(self)
        self.scene.update()

    def redo(self):
        """Redo changes in the app by forwarding to a recorded state.

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
        filename, _ = self._history[self._current]
        filepath = os.path.join(self._tempdir, filename)

        self.scene.clear()
        pre_redo(self)
        self.state = compas.json_load(filepath)
        post_redo(self)
        self.scene.update()

    def save(self):
        """Save the current state of the app to a pickle file.

        Returns
        -------
        None

        """
        if not self.dirname:
            path = FileForm.save(self.dirname, self.basename)
            if not path:
                return

            self.dirname = os.path.dirname(path)
            self.basename = os.path.basename(path)

        path = os.path.join(self.dirname, self.basename)
        compas.json_dump(self.state, path)

    def saveas(self):
        """Save the current state of the app to a pickle file with a specific name.

        Parameters
        ----------
        name : str
            The name of the pickle.

        Returns
        -------
        None

        """
        path = FileForm.save(self.dirname, self.basename)
        if not path:
            return

        self.dirname = os.path.dirname(path)
        self.basename = os.path.basename(path)
        compas.json_dump(self.state, path)

    def load(self):
        """Restore a saved state of the app from a selected pickle file.

        Parameters
        ----------
        name : str
            The name of the shelve.

        Returns
        -------
        None

        """
        path = FileForm.open(self.dirname)
        if not path:
            return

        self.dirname = os.path.dirname(path)
        self.basename = os.path.basename(path)

        self.scene.clear()
        pre_redo(self)
        self.state = compas.json_load(path)
        post_redo(self)
        self.scene.update()
        self.record()

    # ========================================================================
    # User data
    # ========================================================================

    def get_real(self, message, minval=None, maxval=None, default=None):
        """Get a real number from the user.

        Parameters
        ----------
        message : str
            Tell the user what the number is for.
        minval : float, optional
            The minimum value.
        maxval : float, optional
            The maximum value.
        default : float, optional
            The default value.

        Returns
        -------
        float | None

        """
        value = compas_rhino.rs.GetReal(message=message, number=default, minimum=minval, maximum=maxval)
        if value:
            return float(value)

    def get_integer(self, message, minval=None, maxval=None, default=None):
        """Get an integer number from the user.

        Parameters
        ----------
        message : str
            Tell the user what the number is for.
        minval : int, optional
            The minimum value.
        maxval : int, optional
            The maximum value.
        default : int, optional
            The default value.

        Returns
        -------
        int | None

        """
        value = compas_rhino.rs.GetInteger(message=message, number=default, minimum=minval, maximum=maxval)
        if value:
            return int(value)

    def get_string(self, message, options=None, default=None):
        """Get a string from the user.

        Parameters
        ----------
        message : str
            Tell the user what the string is for.
        options : list[str], optional
            A list of options.
        default : str, optional
            The default value.

        Returns
        -------
        str | None

        """
        value = compas_rhino.rs.GetString(message, defaultString=default, strings=options)
        if value:
            return str(value)
