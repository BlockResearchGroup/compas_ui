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
import tempfile

from compas.utilities import flatten

import compas_rhino

from .singleton import Singleton
from .session import Session
from .scene import Scene

from .rhino.forms import BrowserForm
from .rhino.forms import error


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

    @staticmethod
    def error(*args, **kwargs):
        return error(*args, **kwargs)

    def __init__(self, name=None, settings=None):
        if name is None:
            raise RuntimeError(
                'Initialized the app with a name first, for example: app = App(name="my_app")'
            )

        self._current = -1
        self._depth = 20
        self.name = name
        self.dirname = None
        self.basename = "{}.ui".format(self.name)
        self.session = Session(name=self.name)
        self.settings = settings or {}
        self.scene = Scene(settings=self.settings.get("scene"))
        self.proxy = None
        self.start_cloud()

        with open(self.dbname, 'wb') as f:
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

    def clear(self):
        with open(self.dbname, 'wb') as f:
            pickle.dump([], f)
        self.session.reset()
        self.scene.clear()

    def splash(self, url):
        browser = BrowserForm(title=self.name, url=url)
        browser.show()

    # ========================================================================
    # State
    # ========================================================================

    def record(self):
        """Record the current state of the app.

        Returns
        -------
        None

        """
        with open(self.dbname, 'rb') as f:
            history = pickle.load(f)

            if self._current > -1:
                if self._current < len(history) - 1:
                    history = history[:self._current + 1]

            history.append(self.state)
            h = len(history)
            if h > self._depth:
                history = history[h - self._depth:]
            self._current = len(history) - 1

        with open(self.dbname, 'wb') as f:
            pickle.dump(history, f)

    def undo(self):
        """Undo changes in the app by rewinding to a recorded state.

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

        with open(self.dbname, 'rb') as f:
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

        with open(self.dbname, 'rb') as f:
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
        # TODO: move this to a pluggable/plugin

        if not self.dirname:
            import Eto.Forms
            import Rhino.UI
            import System

            dialog = Eto.Forms.SaveFileDialog()
            dialog.Directory = System.Uri(os.path.expanduser("~"))
            dialog.FileName = self.basename

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
        dialog.FileName = self.basename

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

    # ========================================================================
    # User data
    # ========================================================================

    def pick_file(self, basename):
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

        dialog = Eto.Forms.SaveFileDialog()
        dialog.Directory = System.Uri(os.path.expanduser("~"))
        dialog.FileName = basename

        if (
            dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)
            != Eto.Forms.DialogResult.Ok
        ):
            return

        return dialog.FileName

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

    # ========================================================================
    # Selections
    # ========================================================================

    def select_mesh_vertices(self, meshobj):
        """Select vertices of a mesh object through the UI.

        Parameters
        ----------
        meshobj : :class:`compas_ui.objects.MeshObject`

        Returns
        -------
        list[int]

        """
        mesh = meshobj.mesh

        options = ["All", "Boundary", "Corners", "ByContinuousEdges", "Manual"]
        mode = self.get_string(message="Selection mode.", options=options)
        if not mode:
            return

        vertex_guid = {vertex: guid for guid, vertex in iter(meshobj.guid_vertex.items())}

        if mode == 'All':
            vertices = list(mesh.vertices())

        elif mode == 'Boundary':
            vertices = list(set(flatten(mesh.vertices_on_boundaries())))
            guids = [vertex_guid[vertex] for vertex in vertices]
            self.scene.highlight_objects(guids)

        elif mode == "Corners":
            vertices = mesh.corner_vertices()
            guids = [vertex_guid[vertex] for vertex in vertices]
            self.scene.highlight_objects(guids)

        elif mode == "ByContinuousEdges":
            temp = meshobj.select_edges()
            vertices = list(set(flatten([mesh.vertices_on_edge_loop(key) for key in temp])))
            guids = [vertex_guid[vertex] for vertex in vertices]
            self.scene.highlight_objects(guids)

        elif mode == 'Manual':
            vertices = meshobj.select_vertices()

        return vertices

    def select_mesh_edges(self, meshobj):
        """Select edges of a mesh object through the UI.

        Parameters
        ----------
        meshobj : :class:`compas_ui.objects.MeshObject`

        Returns
        -------
        list[tuple[int, int]]

        """
        mesh = meshobj.mesh

        options = ["All", "AllBoundaryEdges", "Continuous", "Parallel", "Manual"]
        mode = self.get_string(message="Selection mode.", options=options)
        if not mode:
            return

        edge_guid = {edge: guid for guid, edge in iter(meshobj.guid_edge.items())}
        edge_guid.update({(v, u): guid for guid, (u, v) in iter(meshobj.guid_edge.items())})

        if mode == 'All':
            edges = list(mesh.edges())

        elif mode == 'AllBoundaryEdges':
            edges = list(set(flatten(mesh.edges_on_boundaries())))
            guids = [edge_guid[edge] for edge in edges]
            self.scene.highlight_objects(guids)

        elif mode == 'Continuous':
            temp = meshobj.select_edges()
            edges = list(set(flatten([mesh.edge_loop(edge) for edge in temp])))
            guids = [edge_guid[edge] for edge in edges]
            self.scene.highlight_objects(guids)

        elif mode == 'Parallel':
            temp = meshobj.select_edges()
            edges = list(set(flatten([mesh.edge_strip(edge) for edge in temp])))
            guids = [edge_guid[edge] for edge in edges]
            self.scene.highlight_objects(guids)

        elif mode == 'Manual':
            edges = meshobj.select_edges()

        return edges
