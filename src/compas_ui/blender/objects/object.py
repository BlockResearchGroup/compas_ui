from compas_ui.objects import Object


class BlenderObject(Object):
    """Base class for COMPAS Blender objects.

    Attributes
    ----------
    layer : str
        The layer for drawing.
        This is an alias for the layer of :attr:BlenderObject.artist`.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._objects = []

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, objects):
        self._objects = objects
