from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
from abc import abstractmethod, abstractproperty
from collections import defaultdict
from copy import deepcopy

import compas
from compas.artists import Artist
from compas.plugins import pluggable
from compas.plugins import PluginValidator

from compas_ui.objects import ObjectNotRegistered


def __copy__(self):
    """Make a shallow copy of the object."""
    item = None
    if hasattr(self, "mesh"):
        item = self.mesh
    elif hasattr(self, "network"):
        item = self.network
    elif hasattr(self, "volmesh"):
        item = self.volmesh
    elif hasattr(self, "shape"):
        item = self.shape
    elif hasattr(self, "primitive"):
        item = self.primitive
    cls = self.__class__
    result = cls.__new__(cls, item)
    result.__dict__.update(self.__dict__)
    return result


def __deepcopy__(self, memo):
    """Make a deep copy of the object."""
    item = None
    if hasattr(self, "mesh"):
        item = self.mesh
    elif hasattr(self, "network"):
        item = self.network
    elif hasattr(self, "volmesh"):
        item = self.volmesh
    elif hasattr(self, "shape"):
        item = self.shape
    elif hasattr(self, "primitive"):
        item = self.primitive
    cls = self.__class__
    result = cls.__new__(cls, item)
    memo[id(self)] = result
    for k, v in self.__dict__.items():
        setattr(result, k, deepcopy(v, memo))
    return result


def __getstate__(self):
    """Return a serializable state of the artist."""
    dictcopy = self.__dict__.copy()

    if "_vertex_color" in self.__dict__:
        if self.__dict__["_vertex_color"] is not None:
            dictcopy["_vertex_color"] = dict(self.__dict__["_vertex_color"])
    if "_node_color" in self.__dict__:
        if self.__dict__["_node_color"] is not None:
            dictcopy["_node_color"] = dict(self.__dict__["_node_color"])
    if "_edge_color" in self.__dict__:
        if self.__dict__["_edge_color"] is not None:
            dictcopy["_edge_color"] = dict(self.__dict__["_edge_color"])
    if "_face_color" in self.__dict__:
        if self.__dict__["_face_color"] is not None:
            dictcopy["_face_color"] = dict(self.__dict__["_face_color"])
    if "_cell_color" in self.__dict__:
        if self.__dict__["_cell_color"] is not None:
            dictcopy["_cell_color"] = dict(self.__dict__["_cell_color"])

    return {"__dict__": dictcopy}


def __setstate__(self, state):
    """Assign a deserialized state to the artist and recreate the descriptors."""
    dictcopy = state["__dict__"].copy()

    if "_vertex_color" in state["__dict__"]:
        dictcopy["_vertex_color"] = None
    if "_node_color" in state["__dict__"]:
        dictcopy["_node_color"] = None
    if "_edge_color" in state["__dict__"]:
        dictcopy["_edge_color"] = None
    if "_face_color" in state["__dict__"]:
        dictcopy["_face_color"] = None
    if "_cell_color" in state["__dict__"]:
        dictcopy["_cell_color"] = None

    self.__dict__.update(dictcopy)

    if "_vertex_color" in state["__dict__"]:
        self.vertex_color = state["__dict__"]["_vertex_color"]
    if "_node_color" in state["__dict__"]:
        self.node_color = state["__dict__"]["_node_color"]
    if "_edge_color" in state["__dict__"]:
        self.edge_color = state["__dict__"]["_edge_color"]
    if "_face_color" in state["__dict__"]:
        self.face_color = state["__dict__"]["_face_color"]
    if "_cell_color" in state["__dict__"]:
        self.cell_color = state["__dict__"]["_cell_color"]


Artist.__copy__ = __copy__
Artist.__deepcopy__ = __deepcopy__
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

    def __init__(self, item, scene=None, name=None, visible=True, settings=None):
        super(Object, self).__init__()
        # self._guids = []
        self._item = None
        self._scene = None
        self._artist = None
        self.item = item
        self.scene = scene
        self.name = name
        self.visible = visible
        self.settings = self.SETTINGS.copy()
        self.settings.update(settings or {})

    def __copy__(self):
        """Make a shallow copy of the object."""
        cls = self.__class__
        result = cls.__new__(cls, self.item)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        """Make a deep copy of the object."""
        cls = self.__class__
        result = cls.__new__(cls, self.item)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __getstate__(self):
        """Return a serializable state of the object."""
        pass

    def __setstate__(self, state):
        """Assign a deserialized state to the object and recreate the descriptors."""
        pass

    # @property
    # def guids(self):
    #     return self._guids

    # @guids.setter
    # def guids(self, guids):
    #     self._guids = guids

    @abstractproperty
    def data(self):
        raise NotImplementedError

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item
        self._guids = []
        self._artist = None

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, scene):
        self._scene = scene

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
