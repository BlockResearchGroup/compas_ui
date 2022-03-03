from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from uuid import uuid4
from compas_ui.objects import Object


# _ITEM_OBJECT = {}


class BaseObject(Object):
    """Abstract base class for COMPAS Rhino objects.

    Parameters
    ----------
    item : {:class:`compas.geometry.Geometry`, :class:`compas.datastructures.Datastructure`}
        A COMPAS geometry object or data structure.
    scene : :class:`compas.scenes.Scene`, optional
        A scene object.
    name : str, optional
        The name of the object.
    layer : str, optional
        The layer for drawing.
    visible : bool, optional
        Toggle for the visibility of the object.
    settings : dict, optional
        A dictionary of settings.

    Attributes
    ----------
    item : {:class:`compas.geometry.Geometry`, :class:`compas.datastructures.Datastructure`}
        A COMPAS geometry object or data structure.
    scene : :class:`compas.scenes.Scene`
        A scene object.
    artist : :class:`compas_rhino.artists.Artist`
        The artist matching the type of ``item``.
    name : str
        The name of the object.
        This is an alias for the name of ``item``.
    layer : str
        The layer for drawing.
        This is an alias for the layer of ``artist``.
    visible : bool
        Toggle for the visibility of the object in the scene.
    settings : dict
        A dictionary of settings related to visualisation and interaction.
        This dict starts from the settings of the ``artist``.

    """

    def __init__(self, item, scene=None, name=None, layer=None, visible=True, settings=None):
        super(BaseObject, self).__init__(item)
        self._id = None
        self._scene = None
        self.scene = scene
        self.name = name
        self.layer = layer
        self.visible = visible
        self.settings = settings or {}

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, scene):
        self._scene = scene

    @property
    def id(self):
        if not self._id:
            self._id = uuid4()
        return self._id

    @property
    def layer(self):
        return self.artist.layer

    @layer.setter
    def layer(self, layer):
        self.artist.layer = layer

    # ==========================================================================
    # Methods
    # ==========================================================================

    def clear(self):
        """Clear all previously created Rhino objects."""
        raise NotImplementedError

    def clear_layer(self):
        """Clear the layer of the object."""
        self.artist.clear_layer()

    def draw(self):
        """Draw the object representing the item."""
        raise NotImplementedError

    def redraw(self):
        """Redraw the Rhino scene/view."""
        self.artist.redraw()

    def select(self):
        """Select the object representing the item."""
        raise NotImplementedError

    def modify(self):
        """Modify the item represented by the object."""
        raise NotImplementedError

    def move(self):
        """Move the item represented by the object."""
        raise NotImplementedError
