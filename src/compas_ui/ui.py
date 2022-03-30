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

    def __init__(self, config=None, controller_class=None):
        if config is None:
            raise RuntimeError(
                "Initialized the UI with a configuration dict first, for example: ui = UI(config={...})"
            )

        controller_class = controller_class or Controller

        self._current = -1
        self._depth = 20

        self.config = config
        self.name = self.config["plugin"]["title"]
        self.condadir = None
        self.dirname = None
        self.basename = "{}.ui".format(self.name)
        self.settings = self.config["settings"] or {}

        self.session = Session(name=self.name)
        self.scene = Scene(settings=self.settings.get("scene"))
        self.controller = controller_class(self)
        self.proxy = None

        with open(self.dbname, "wb") as f:
            pickle.dump([], f)
        self.record()

    @property
    def dbname(self):
        return os.path.join(tempfile.gettempdir(), "{}.history".format(self.name))

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

    def splash(self, url):
        """Display a splash screen.

        Parameters
        ----------
        url : str
            The url of the html file.

        Returns
        -------
        None

        """
        from .rhino.forms import SplashForm

        browser = SplashForm(title=self.name, url=url)
        browser.show()

    def about(self):
        """Display a standard dialog with information about the project.

        Returns
        -------
        None

        """
        import System
        import Eto.Forms
        import Rhino.UI

        dialog = Eto.Forms.AboutDialog()

        dialog.Copyright = self.config["plugin"]["copyright"]
        dialog.Designers = System.Array[System.String](
            self.config["plugin"]["designers"]
        )
        dialog.Developers = System.Array[System.String](
            self.config["plugin"]["developers"]
        )
        dialog.Documenters = System.Array[System.String](
            self.config["plugin"]["documenters"]
        )
        dialog.License = self.config["plugin"]["license"]
        dialog.ProgramDescription = self.config["plugin"]["description"]
        dialog.ProgramName = self.config["plugin"]["title"]
        dialog.Title = self.config["plugin"]["title"]
        dialog.Version = self.config["plugin"]["version"]
        dialog.Website = System.Uri(self.config["plugin"]["website"])

        dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)

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
        from .rhino.forms import CondaEnvsForm

        if not self.condadir:
            import Rhino.UI
            import Eto.Forms

            dialog = Eto.Forms.SelectFolderDialog()
            dialog.Directory = os.path.expanduser("~")

            result = dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)
            if result != Eto.Forms.DialogResult.Ok:
                return
            if not dialog.Directory:
                return

            self.condadir = dialog.Directory

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
            if parts:
                envs.append((parts[0], parts[-1]))

        form = CondaEnvsForm(envs)
        form.show()

    def conda_activate(self):
        """Activate a conda environment by running a subprocess that does a compas_rhino install.

        Returns
        -------
        None

        """
        pass

    def rhinopython_searchpaths(self):
        """Modify the Rhino Python search paths.

        Returns
        -------
        None

        """
        import System
        import Rhino.UI

        from .rhino.forms import SearchPathsForm

        dialog = SearchPathsForm()

        if not dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow):
            return

        paths = []
        for path in Rhino.Runtime.PythonScript.SearchPaths:
            paths.append(path)
        paths[:] = paths[:3]
        for row in dialog.data:
            path = row[0]
            path = path.strip()
            if path:
                paths.append(path)

        paths = System.Array[System.String](paths)
        Rhino.Runtime.PythonScript.SearchPaths = paths

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

    def scene_update(self):
        """Update the scene.

        Returns
        -------
        None

        """
        self.scene.update()

    def scene_objects(self):
        """Display a form with all objects in the scene.

        Returns
        -------
        None

        """
        from .rhino.forms import SceneObjectsForm

        form = SceneObjectsForm(self.scene)
        form.show()

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
        """Save the current state of the app to a pickle file.

        Returns
        -------
        None

        """
        if not self.dirname:
            from .rhino.forms import FileForm

            path = FileForm.save(self.dirname, self.basename)
            if not path:
                return

            self.dirname = os.path.dirname(path)
            self.basename = os.path.basename(path)

        path = os.path.join(self.dirname, self.basename)

        with open(path, "wb+") as f:
            pickle.dump(self.state, f)

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
        from .rhino.forms import FileForm

        path = FileForm.save(self.dirname, self.basename)
        if not path:
            return

        self.dirname = os.path.dirname(path)
        self.basename = os.path.basename(path)

        with open(path, "wb+") as f:
            pickle.dump(self.state, f)

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
        from .rhino.forms import FileForm

        path = FileForm.open(self.dirname or os.path.expanduser("~"))
        if not path:
            return

        self.dirname = os.path.dirname(path)
        self.basename = os.path.basename(path)

        with open(path, "rb") as f:
            self.state = pickle.load(f)

        self.scene.clear()
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
        from compas_ui.rhino.forms.settings import SettingsForm

        form = SettingsForm(self.settings)
        if form.show():
            self.settings.update(form.settings)
            self.scene.update()

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
        value = compas_rhino.rs.GetString(
            message, defaultString=default, strings=options
        )
        if value:
            return str(value)
