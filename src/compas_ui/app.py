"""
********************************************************************************
app
********************************************************************************

.. currentmodule:: compas_ui.app


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    App

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle

import compas_rhino

from .singleton import Singleton
from .session import Session
from .scene import Scene


class App(Singleton):
    """App singleton.

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

    @staticmethod
    def reset():
        App._instances = {}

    def __init__(self, name=None, settings=None):
        if name is None:
            raise RuntimeError(
                'Initialized the app with a name first, for example: app = App(name="my_app")'
            )

        self.name = name
        self.dirname = None
        self.basename = "{}.app".format(self.name)
        self.session = Session(name=self.name)
        self.settings = settings or {}
        self.scene = Scene(settings=self.settings.get("scene"))
        self.proxy = None
        self.start_cloud()

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

    def start_cloud(self):
        """Start the command server.

        Returns
        -------
        None

        Raises
        ------
        ImportError
            If `compas_cloud` is not installed.

        """
        cloud_settings = self.settings.get("cloud")
        if cloud_settings is not None:
            try:
                from compas_cloud import Proxy

                self.proxy = Proxy(**cloud_settings)
            except ImportError:
                raise ImportError("The compas_cloud package is not installed.")

    def record(self):
        """Record the current state of the app.

        Returns
        -------
        None

        """
        self.session.record()
        self.scene.record()

    def undo(self):
        """Undo changes in the app by rewinding to a recorded state.

        Returns
        -------
        None

        """
        self.session.undo()
        self.scene.undo()

    def redo(self):
        """Redo changes in the app by forwarding to a recorded state.

        Returns
        -------
        None

        """
        self.session.redo()
        self.scene.redo()

    def save(self):
        """Save the current state of the app to a shelve.

        Returns
        -------
        None

        """
        # TODO: move this to a pluggable/plugin

        if not self.dirname or not self.basename:
            import Eto.Forms
            import Rhino.UI
            import System

            dialog = Eto.Forms.SaveFileDialog()
            dialog.Directory = System.Uri(os.path.expanduser("~"))
            dialog.FileName = "{}.app".format(self.name)

            if (
                dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)
                != Eto.Forms.DialogResult.Ok
            ):
                return

            path = dialog.FileName
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
        # TODO: move this to a pluggable/plugin

        import Eto.Forms
        import Rhino.UI
        import System

        dialog = Eto.Forms.SaveFileDialog()
        dialog.Directory = System.Uri(os.path.expanduser("~"))
        dialog.FileName = "{}.app".format(self.name)

        if (
            dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)
            != Eto.Forms.DialogResult.Ok
        ):
            return

        path = dialog.FileName
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
        # TODO: move this to a pluggable/plugin

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

        self.scene.clear()

        path = dialog.FileName
        self.dirname = os.path.dirname(path)
        self.basename = os.path.basename(path)

        with open(path, "rb") as f:
            self.state = pickle.load(f)

        self.scene.update()

    def update_settings(self):
        """Update the settings of the app.

        Returns
        -------
        None

        """
        # TODO: move this to a pluggable/plugin

        from compas_ui.rhino.forms.settings import SettingsForm

        form = SettingsForm(self.settings)
        form.show()

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
        # TODO: move this to a pluggable/plugin

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
        # TODO: move this to a pluggable/plugin

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
        # TODO: move this to a pluggable/plugin

        value = compas_rhino.rs.GetString(message, defaultString=default, strings=options)
        if value:
            return str(value)
