from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import shelve

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

    def __init__(self, name=None, settings=None):
        if name is None:
            raise RuntimeError('Initialized the app with a name first, for example: app = App(name="my_app")')

        self.name = name
        self.session = Session(name=self.name)
        self.settings = settings or {}
        self.scene = Scene(settings=self.settings.get('scene'))
        self.proxy = None
        self.start_cloud()

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
        cloud_settings = self.settings.get('cloud')
        if cloud_settings is not None:
            try:
                from compas_cloud import Proxy
                self.proxy = Proxy(**cloud_settings)
            except ImportError:
                raise ImportError('The compas_cloud package is not installed.')

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
        db = shelve.open(self.name)
        try:
            db['session'] = self.session.data
            db['scene'] = self.scene.state
            db['settings'] = self.settings
        except Exception:
            raise
        finally:
            db.close()

    def saveas(self, name):
        """Save the current state of the app to a shelve with a specific name.

        Parameters
        ----------
        name : str
            The name of the shelve.

        Returns
        -------
        None

        """
        db = shelve.open(name)
        try:
            db['session'] = self.session.data
            db['scene'] = self.scene.state
            db['settings'] = self.settings
        except Exception:
            pass
        finally:
            db.close()

    def load(self, name):
        """Restore a saved state of the app from a shelve with a specific name.

        Parameters
        ----------
        name : str
            The name of the shelve.

        Returns
        -------
        None

        """
        self.scene.clear()
        db = shelve.open(name)
        try:
            self.session.data = db['session']
            self.scene.state = db['scene']
            self.settings = db['settings']
        except Exception:
            pass
        finally:
            db.close()
