from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .singleton import Singleton
from .session import Session


@Singleton
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

    def __init__(self, scene=None, proxy=None):
        self.scene = scene
        self.proxy = proxy
        self.session = Session()
