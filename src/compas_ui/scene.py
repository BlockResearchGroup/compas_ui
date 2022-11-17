"""
********************************************************************************
scene
********************************************************************************

.. currentmodule:: compas_ui.scene


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Scene

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import pluggable

from compas_ui.objects import Object
from compas_ui.singleton import Singleton
import uuid


@pluggable(category="ui")
def update_scene(self):
    raise NotImplementedError


@pluggable(category="ui")
def clear_scene(self):
    raise NotImplementedError


@pluggable(category="ui")
def highlight_objects(self):
    raise NotImplementedError


class Scene(Singleton):
    """The scene singleton keeps track of the view objects of an app.

    Parameters
    ----------
    settings : dict[str, Any], optional
        Visualization settings of the scene.

    Attributes
    ----------
    state : dict[str, Any]
        The current state of the scene, containing the objects and the scene settings.
    objects : list[:class:`compas_ui.objects.Object`]
        The objects in the scene.
    settings : dict[str, Any]
        The visualization settings.
    active_object : :class:`compas_ui.objects.Object`
        The active object that is currently being operated on.

    """

    SETTINGS = {}

    def __init__(self, settings=None):
        super(Scene, self).__init__()
        self.objects = []
        self.settings = Scene.SETTINGS.copy()
        self.settings.update(settings or {})
        self._active_object = None

    @property
    def state(self):
        data = {}
        objects = []
        for obj in self.objects:
            objstate = obj.state
            if objstate["item"] not in data:
                data[objstate["item"]] = obj.item
            objects.append(objstate)
        return {
            "data": data,
            "objects": objects,
            "settings": self.settings,
        }

    @state.setter
    def state(self, state):
        self.objects = []
        for objstate in state["objects"]:
            item = state["data"][objstate["item"]]
            obj = self.add(
                item,
                name=objstate["name"],
                visible=objstate["visible"],
                settings=objstate["settings"],
            )
            obj._guid = uuid.UUID(objstate["guid"])

            # TODO: clean this up later.
            if "anchor" in objstate:
                obj.anchor = objstate["anchor"]
            if "location" in objstate:
                obj.location = objstate["location"]
            if "scale" in objstate:
                obj.scale = objstate["scale"]
            if "rotation" in objstate:
                obj.rotation = objstate["rotation"]

        for objstate in state["objects"]:
            if objstate["parent"]:
                obj = self.get_by_guid(objstate["guid"])
                obj.parent = self.get_by_guid(objstate["parent"])
        self.settings = Scene.SETTINGS.copy()
        self.settings.update(state["settings"])

    @property
    def active_object(self):
        return self._active_object

    @active_object.setter
    def active_object(self, obj):
        if isinstance(obj, Object):
            self._active_object = obj
        elif obj is None:
            self._active_object = None
        else:
            raise TypeError("The active object must be a compas_ui.objects.Object.")

    def add(self, item, **kwargs):
        """Add a COMPAS data item to the scene.

        Parameters
        ----------
        item : :class:`compas.data.Data`
            A COMPAS data item/object.
        **kwargs : dict[str, Any], optional
            Additional parameters to be passed on to the scene object corresponding to the data item.

        Returns
        -------
        :class:`compas_ui.objects.Object`

        """
        obj = Object(item, scene=self, **kwargs)
        self.objects.append(obj)
        self.active_object = obj
        return obj

    def remove(self, obj):
        obj.clear()
        while obj in self.objects:
            self.objects.remove(obj)

    def get(self, name):
        """Get all scene objects with a given name.

        Parameters
        ----------
        name : str
            The name of the object(s).

        Returns
        -------
        list[:class:`compas_ui.objects.Object`]

        """
        objects = []
        for obj in self.objects:
            if name == obj.name:
                objects.append(obj)
        return objects

    def get_by_guid(self, guid):
        """Get a scene object by its guid.

        Parameters
        ----------
        name : str
            The guid of the object.

        Returns
        -------
        :class:`compas_ui.objects.Object`

        """
        guid = uuid.UUID(guid)
        for obj in self.objects:
            if guid == obj.guid:
                return obj

    def update(self):
        """Update the scene.

        Returns
        -------
        None

        """
        update_scene(self)

    def clear(self):
        """Clear the scene.

        Returns
        -------
        None

        """
        clear_scene(self)

    def highlight_objects(self, guids):
        """Highlight objects in the scene.

        Returns
        -------
        None

        """
        highlight_objects(self, guids)
