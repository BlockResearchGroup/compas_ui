from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
from uuid import uuid4
from abc import abstractmethod
from collections import defaultdict

import compas
from compas.artists import Artist
from compas.plugins import pluggable
from compas.plugins import PluginValidator

from compas_ui.objects import ObjectNotRegistered

def __getstate__(self):
    """Return a serializable state of the artist."""
    state = self.__dict__.copy()

    if "_vertex_color" in self.__dict__:
        if self.__dict__["_vertex_color"] is not None:
            state["_vertex_color"] = dict(self.__dict__["_vertex_color"])
    if "_node_color" in self.__dict__:
        if self.__dict__["_node_color"] is not None:
            state["_node_color"] = dict(self.__dict__["_node_color"])
    if "_edge_color" in self.__dict__:
        if self.__dict__["_edge_color"] is not None:
            state["_edge_color"] = dict(self.__dict__["_edge_color"])
    if "_face_color" in self.__dict__:
        if self.__dict__["_face_color"] is not None:
            state["_face_color"] = dict(self.__dict__["_face_color"])
    if "_cell_color" in self.__dict__:
        if self.__dict__["_cell_color"] is not None:
            state["_cell_color"] = dict(self.__dict__["_cell_color"])

    return state


def __setstate__(self, state):
    """Assign a deserialized state to the artist and recreate the descriptors."""

    original = state.copy()

    if "_vertex_color" in state:
        state["_vertex_color"] = None
    if "_node_color" in state:
        state["_node_color"] = None
    if "_edge_color" in state:
        state["_edge_color"] = None
    if "_face_color" in state:
        state["_face_color"] = None
    if "_cell_color" in state:
        state["_cell_color"] = None

    self.__dict__.update(state)

    if "_vertex_color" in original:
        self.vertex_color = original["_vertex_color"]
    if "_node_color" in state:
        self.node_color = original["_node_color"]
    if "_edge_color" in state:
        self.edge_color = original["_edge_color"]
    if "_face_color" in state:
        self.face_color = original["_face_color"]
    if "_cell_color" in state:
        self.cell_color = original["_cell_color"]


Artist.__getstate__ = __getstate__
Artist.__setstate__ = __setstate__


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
            "No object is registered for this data type: {} in this context: {}".format(
                dtype, Object.CONTEXT
            )
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
    SETTINGS = {}

    def __new__(cls, *args, **kwargs):
        if not Object.__OBJECTS_REGISTERED:
            register_objects()
            Object.__OBJECTS_REGISTERED = True
        cls = _get_object_cls(args[0], **kwargs)
        PluginValidator.ensure_implementations(cls)
        return super(Object, cls).__new__(cls)

    def __init__(self, item, name=None, visible=True, settings=None):
        super(Object, self).__init__()
        self._guid = None
        self._item = None
        self._artist = None
        self.speckle_id = None
        self.item = item
        self.name = name
        self.visible = visible
        self.settings = self.SETTINGS.copy()
        self.settings.update(settings or {})

    def __getstate__(self):
        return self.state

    def __setstate__(self, state):
        self.state = state

    @property
    def state(self):
        state = self.__dict__.copy()
        for name in state:
            if name.startswith('_conduit'):
                state[name] = None
            elif name == '_artist':
                state[name] = None
            elif name == '_scene':
                state[name] = None
        return state

    @state.setter
    def state(self, state):
        for name in state:
            if name.startswith('_conduit'):
                state[name] = None
            elif name == '_artist':
                state[name] = None
            elif name == '_scene':
                state[name] = None
        self.__dict__.update(state)

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

    def speckle_push(self):
        from compas_ui.ui import UI
        self.speckle_id = UI().proxy.speckle_push(stream_id=self.state['speckle_id'], item=self.state)
        return self.speckle_id
    
    def speckle_pull(self):
        from compas_ui.ui import UI
        self.state = UI().proxy.speckle_pull(stream_id=self.state['speckle_id'])
        return self.state
