from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .session import Session


class App(object):
    """App singleton.

    Parameters
    ----------
    scene : :class:`compas_ui.scene.Scene`, optional
        The compas_ui scene object.
    proxy : Union[:class:`compas_cloud.Proxy`, :class:`compas.rpc.Proxy`], optional
        The compas rpc or compas_cloud Proxy object.

    Attributes
    ----------
    scene : :class:`compas_ui.scene.Scene`
        The compas_ui scene object.
    proxy : Union[:class:`compas_cloud.Proxy`, :class:`compas.rpc.Proxy`]
        The compas rpc or compas_cloud Proxy object.
    session : :class:`compas_ui.session.Session`
        The compas_ui session object.

    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            self = super(App, cls).__new__(cls)
            self._initialized = False
            cls._instance = self
        return cls._instance

    def __init__(self, scene=None, proxy=None):
        if self._initialized:
            return
        self.scene = scene
        self.proxy = proxy
        self.session = Session()
        self._initialized = True

    @classmethod
    def initialized(cls):
        return cls._instance is not None and cls._instance._initialized
