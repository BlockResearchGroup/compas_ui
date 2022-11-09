from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
import uuid
from uuid import uuid4
from abc import abstractmethod
from collections import defaultdict

import compas
from compas.artists import Artist
from compas.plugins import pluggable
from compas.plugins import PluginValidator

from compas_ui.objects import ObjectNotRegistered
from compas_ui.values import Settings


@pluggable(category="ui", selector="collect_all")
def register_objects():
    raise NotImplementedError


def identify_context():
    if compas.is_grasshopper():
        return "Grasshopper"
    if compas.is_rhino():
        return "Rhino"
    if compas.is_blender():
        return "Blender"
    return None


def _get_object_cls(data, **kwargs):
    if "context" in kwargs:
        Object.CONTEXT = kwargs["context"]
    else:
        Object.CONTEXT = identify_context()

    dtype = type(data)
    cls = None

    if "object_type" in kwargs:
        cls = kwargs["object_type"]
    else:
        context = Object.ITEM_OBJECT[Object.CONTEXT]
        for type_ in inspect.getmro(dtype):
            cls = context.get(type_, None)
            if cls is not None:
                break

    if cls is None:
        raise ObjectNotRegistered(
            "No object is registered for this data type: {} in this context: {}".format(dtype, Object.CONTEXT)
        )

    return cls


class Object(object):
    """Base class for all objects.

    Parameters
    ----------
    item : :class:`compas.data.Data`
        A COMPAS data object.
    scene : :class:`compas.scenes.Scene`, optional
        A scene object.
    name : str, optional
        The name of the object.
    visible : bool, optional
        Toggle for the visibility of the object.
    settings : dict[str, Any], optional
        A dictionary of settings.

    Attributes
    ----------
    item : :class:`compas.data.Data`
        The COMPAS data object assignd to this scene object.
    scene : :class:`compas.scenes.Scene`
        The scene.
    artist : :class:`compas.artists.Artist`
        The artist matching the type of `item`.
    name : str
        The name of the object.
        This is an alias for the name of `item`.
    visible : bool
        Toggle for the visibility of the object in the scene.
    settings : dict
        A dictionary of settings related to visualisation and interaction.
        This dict starts from the settings of the `artist`.

    """

    __OBJECTS_REGISTERED = False

    AVAILABLE_CONTEXTS = [
        "Rhino",
    ]
    CONTEXT = None
    ITEM_OBJECT = defaultdict(dict)
    SETTINGS = Settings()

    def __new__(cls, *args, **kwargs):
        if not Object.__OBJECTS_REGISTERED:
            register_objects()
            Object.__OBJECTS_REGISTERED = True
        cls = _get_object_cls(args[0], **kwargs)
        PluginValidator.ensure_implementations(cls)
        return super(Object, cls).__new__(cls)

    def __init__(self, item, scene=None, name=None, visible=True, settings=None):
        super(Object, self).__init__()
        self._guid = None
        self._item = None
        self._artist = None
        self._scene = scene
        self.item = item
        self.name = name
        self.visible = visible
        self.settings = self.SETTINGS.copy()
        self.settings.update(settings or {})
        self.parent = None

    def __getstate__(self):
        return self.state

    def __setstate__(self, state):
        self.state = state

    @property
    def state(self):
        return {
            "guid": str(self.guid),
            "name": self.name,
            "item": str(self.item.guid),
            "parent": str(self.parent.guid) if self.parent else None,
            "settings": self.settings,
            "artist": self.artist.state,
            "visible": self.visible,
        }

    @state.setter
    def state(self, state):
        self._guid = uuid.UUID(state["guid"])
        self.name = state["name"]
        self.settings.update(state["settings"])
        self.artist.state = state["artists"]
        self.visible = state["visible"]
        # parent?
        # item?

    @property
    def children(self):
        return list(filter(lambda x: x.parent == self, self._scene.objects))

    def add(self, item, **kwargs):
        if isinstance(item, Object):
            obj = item
        else:
            obj = self._scene.add(item, **kwargs)
        obj.parent = self
        return obj

    def remove(self, obj):
        obj = self._scene.remove(obj)

    @property
    def active(self):
        if self._scene:
            return self._scene.active_object is self
        else:
            return False

    @property
    def guid(self):
        if not self._guid:
            self._guid = uuid4()
        return self._guid

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item
        self._artist = None

    @property
    def artist(self):
        if not self._artist:
            self._artist = Artist(self.item)
        return self._artist

    @staticmethod
    def register(item_type, object_type, context=None):
        Object.ITEM_OBJECT[context][item_type] = object_type

    @abstractmethod
    def clear(self):
        raise NotImplementedError

    @abstractmethod
    def draw(self):
        raise NotImplementedError

    # not sure this should exist
    def redraw(self):
        self.artist.redraw()

    def select(self):
        raise NotImplementedError

    def modify(self):
        raise NotImplementedError

    def move(self):
        raise NotImplementedError
