from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_ui.objects import Object


class RhinoObject(Object):
    """Base class for COMPAS Rhino objects.

    Attributes
    ----------
    layer : str
        The layer for drawing.
        This is an alias for the layer of :attr:RhinoObject.artist`.

    """

    def __init__(self, *args, **kwargs):
        super(RhinoObject, self).__init__(*args, **kwargs)
        self._guids = []

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def guids(self):
        return self._guids

    @guids.setter
    def guids(self, guids):
        self._guids = guids
