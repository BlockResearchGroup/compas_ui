from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_ui.objects import Object


class RhinoObject(Object):
    """Base class for COMPAS Rhino objects.

    Parameters
    ----------
    layer : str, optional
        The layer for drawing.

    Attributes
    ----------
    layer : str
        The layer for drawing.
        This is an alias for the layer of :attr:RhinoObject.artist`.

    """

    def __init__(self, *args, layer=None, **kwargs):
        super(RhinoObject, self).__init__(*args, **kwargs)
        self.layer = layer

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def layer(self):
        return self.artist.layer

    @layer.setter
    def layer(self, layer):
        self.artist.layer = layer

    # ==========================================================================
    # Methods
    # ==========================================================================

    def clear_layer(self):
        """Clear the layer of the object."""
        self.artist.clear_layer()
