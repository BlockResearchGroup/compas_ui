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
import pickle
import tempfile
from subprocess import Popen
from subprocess import PIPE

import compas_rhino

from compas_cloud import Proxy

from .singleton import Singleton
from .session import Session
from .scene import Scene
from .controller import Controller


class UI(Singleton):
    """UI singleton.

    Parameters
    ----------
    name : str
        The name of the app.
    settings : settings for scene and proxy object, optional
        The compas rpc or compas_cloud Proxy object.

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

    def __init__(self, name=None, settings=None, controller_class=None):
        if name is None:
            raise RuntimeError(
                'Initialized the UI with a name first, for example: ui = UI(name="MyUI")'
            )

        controller_class = controller_class or Controller

        self._current = -1
        self._depth = 20
        self.name = name
        self.dirname = None
        self.basename = "{}.ui".format(self.name)
        self.session = Session(name=self.name)
        self.settings = settings or {}
        self.scene = Scene(settings=self.settings.get("scene"))
        self.controller = controller_class(self)
        self.proxy = None
        self.condadir = None
        with open(self.dbname, "wb") as f:
            pickle.dump([], f)
        self.record()

    @property
    def dbname(self):
        return os.path.join(tempfile.gettempdir(), "{}.history".format(self.basename))

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
        with open(self.dbname, "wb") as f:
            pickle.dump([], f)
        self.session.reset()
        self.scene.clear()

    # ========================================================================
    # Info
    # ========================================================================

    @staticmethod
    def error(*args, **kwargs):
        from .rhino.forms import error

        return error(*args, **kwargs)

    def splash(self, url):
        from .rhino.forms import BrowserForm

        browser = BrowserForm(title=self.name, url=url)
        browser.show()

    def github(self):
        print("Go to github.")

    def docs(self):
        print("Go to the docs.")

    def examples(self):
        print("Go to the examples.")

    # ========================================================================
    # Cloud
    # ========================================================================

    def cloud_start(self):
        """Start the command server.

        Returns
        -------
        None

        Raises
        ------
        ImportError
            If `compas_cloud` is not installed.

        """
        settings = self.settings.get("cloud") or {}
        self.proxy = Proxy(**settings)

    def cloud_restart(self):
        self.proxy.restart()

    def cloud_shutdown(self):
        self.proxy.shutdown()

    def speckle_sync(self):
        pass

    # ========================================================================
    # Scene
    # ========================================================================

    def scene_clear(self):
        self.scene.clear()

    def scene_update(self):
        self.scene.update()

    def scene_objects(self):
        for obj in self.scene.objects:
            print(obj.name, obj.item, obj.settings)

    # ========================================================================
    # Conda
    # ========================================================================

    def conda_envs(self):
        if not self.condadir:
            user = os.path.expanduser("~")
            condadir = self.pick_file_open(user)
            if not condadir:
                return
            self.condadir = condadir

        conda = os.path.join(self.condadir, "condabin", "conda")
        process = Popen(["{} info --envs".format(conda)], stdout=PIPE, shell=True)
        out = process.stdout.read().decode()
        lines = out.split("\n")
        envs = []
        for line in lines:
            if line.startswith("#"):
                continue
            parts = lines.split()
            envs.append((parts[0], parts[-1]))
        for name, path in sorted(envs, key=lambda env: env[0]):
            print(name, path)

    def conda_activate(self):
        pass

    # ========================================================================
    # State
    # ========================================================================

    def record(self):
        """Record the current state of the UI.

        Returns
        -------
        None

        """
        with open(self.dbname, "rb") as f:
            history = pickle.load(f)

            if self._current > -1:
                if self._current < len(history) - 1:
                    history = history[: self._current + 1]

            history.append(self.state)
            h = len(history)
            if h > self._depth:
                history = history[h - self._depth :]  # noqa : E203
            self._current = len(history) - 1

        with open(self.dbname, "wb") as f:
            pickle.dump(history, f)

    def undo(self):
        """Undo changes in the UI by rewinding to a recorded state.

        Returns
        -------
        None

        """
        self.scene.clear()

        if self._current < 0:
            print("Nothing to undo!")
            return

        if self._current == 0:
            print("Nothing more to undo!")
            return

        with open(self.dbname, "rb") as f:
            history = pickle.load(f)

        self._current -= 1
        self.state = history[self._current]

        self.scene.update()

    def redo(self):
        """Redo changes in the app by forwarding to a recorded state.

        Returns
        -------
        None

        """
        self.scene.clear()

        if self._current < 0:
            print("Nothing to redo!")
            return

        with open(self.dbname, "rb") as f:
            history = pickle.load(f)

        if self._current == len(history) - 1:
            print("Nothing more to redo!")
            return

        self._current += 1
        self.state = history[self._current]

        self.scene.update()

    def save(self):
        """Save the current state of the app to a shelve.

        Returns
        -------
        None

        """
        if not self.dirname:
            path = self.pick_file_save(self.basename)
            if not path:
                return

            self.dirname = os.path.dirname(path)
            self.basename = os.path.basename(path)

        else:
            path = os.path.join(self.dirname, self.basename)

        with open(path, "wb+") as f:
            pickle.dump(self.state, f)

    def saveas(self):
        """Save the current state of the app to a shelve with a specific name.

        Parameters
        ----------
        name : str
            The name of the shelve.

        Returns
        -------
        None

        """
        path = self.pick_file_save(self.basename)
        if not path:
            return

        self.dirname = os.path.dirname(path)
        self.basename = os.path.basename(path)

        with open(path, "wb+") as f:
            pickle.dump(self.state, f)

    def load(self):
        """Restore a saved state of the app from a shelve with a specific name.

        Parameters
        ----------
        name : str
            The name of the shelve.

        Returns
        -------
        None

        """
        path = self.pick_file_open(self.dirname)
        if not path:
            return

        self.scene.clear()

        self.dirname = os.path.dirname(path)
        self.basename = os.path.basename(path)

        with open(path, "rb") as f:
            self.state = pickle.load(f)

        self.scene.update()

    # ========================================================================
    # Settings
    # ========================================================================

    def update_settings(self):
        """Update the settings of the app.

        Returns
        -------
        None

        """
        # TODO: move this to a pluggable/plugin

        from compas_ui.rhino.forms.settings import SettingsForm

        form = SettingsForm(self.settings)
        if form.show():
            self.settings.update(form.settings)
            self.scene.update()

    # ========================================================================
    # User data
    # ========================================================================

    def pick_file_save(self, basename):
        """Pick a file on the file system.

        Parameters
        ----------
        basename : str
            The basename of the file.

        Returns
        -------
        path

        """
        import Eto.Forms
        import Rhino.UI
        import System

        dirname = self.dirname or os.path.expanduser("~")

        dialog = Eto.Forms.SaveFileDialog()
        dialog.Directory = System.Uri(dirname)
        dialog.FileName = basename

        if (
            dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)
            != Eto.Forms.DialogResult.Ok
        ):
            return

        return dialog.FileName

    def pick_file_open(self, dirname):
        """Pick a file on the file system.

        Returns
        -------
        path

        """
        import Eto.Forms
        import Rhino.UI
        import System

        dirname = self.dirname or os.path.expanduser("~")

        dialog = Eto.Forms.OpenFileDialog()
        dialog.Directory = System.Uri(dirname)
        dialog.MultiSelect = False

        if (
            dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)
            != Eto.Forms.DialogResult.Ok
        ):
            return

        return dialog.FileName

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
        # TODO: move this to a pluggable/plugin

        value = compas_rhino.rs.GetReal(
            message=message, number=default, minimum=minval, maximum=maxval
        )
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
        # TODO: move this to a pluggable/plugin

        value = compas_rhino.rs.GetInteger(
            message=message, number=default, minimum=minval, maximum=maxval
        )
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
        # TODO: move this to a pluggable/plugin

        value = compas_rhino.rs.GetString(
            message, defaultString=default, strings=options
        )
        if value:
            return str(value)
