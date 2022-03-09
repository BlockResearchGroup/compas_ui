from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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

    """

    def __init__(self, name=None, settings=None):
        if name is None:
            raise RuntimeError('Initialized the app with a name first, for example: app = App(name="my_app")')

        self.name = name
        self.settings = settings or {}
        self.data = Session(name=self.name)
        self.scene = Scene(settings=self.settings.get('scene') or {})
        self.proxy = None
        self.start_cloud()

    def start_cloud(self):
        cloud_settings = self.settings.get('cloud')
        if cloud_settings is not None:
            try:
                from compas_cloud import Proxy
                self.proxy = Proxy(**cloud_settings)
            except ImportError:
                raise ImportError('The compas_cloud package is not installed.')

    def record(self):
        self.data.record()

    def undo(self):
        self.data.undo()
        self.scene.update()

    def redo(self):
        pass

    def save(self):
        pass

    def saveas(self):
        pass

    def load(self):
        pass
