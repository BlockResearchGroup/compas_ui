from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import System
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
        guids = []
        for guid in self._guids:
            if isinstance(guid, System.Guid):
                guids.append(guid)
            elif isinstance(guid, str):
                result, guid = System.Guid.TryParse(guid)
                if result:
                    guids.append(guid)
        return guids

    @guids.setter
    def guids(self, guids):
        self._guids = guids
