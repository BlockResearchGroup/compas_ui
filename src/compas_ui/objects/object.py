from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
from abc import abstractmethod
from collections import defaultdict

import compas
from compas.data import Data
from compas.artists import Artist
from compas_ui.objects import DataObjectNotRegistered
from compas.plugins import pluggable
from compas.plugins import PluginValidator


@pluggable(category='ui', selector='collect_all')
def register_objects():
    raise NotImplementedError


def identify_context():
    if compas.is_grasshopper():
        return 'Grasshopper'
    if compas.is_rhino():
        return 'Rhino'
    if compas.is_blender():
        return 'Blender'
    return None


def _get_object_cls(data, **kwargs):
    if 'context' in kwargs:
        Object.CONTEXT = kwargs['context']
    else:
        Object.CONTEXT = identify_context()

    dtype = type(data)
    cls = None

    if 'object_type' in kwargs:
        cls = kwargs['object_type']
    else:
        context = Object.ITEM_OBJECT[Object.CONTEXT]
        for type_ in inspect.getmro(dtype):
            cls = context.get(type_, None)
            if cls is not None:
                break

    if cls is None:
        raise DataObjectNotRegistered('No object is registered for this data type: {} in this context: {}'.format(dtype, Object.CONTEXT))

    return cls


class Object(Data):
    """Base class for all objects.
    """

    __OBJECTS_REGISTERED = False

    AVAILABLE_CONTEXTS = ['Rhino', 'Blender', 'Viewer']
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

    def __init__(self, item, name=None, *args, **kwargs):
        super(Object, self).__init__()
        self._ids = []
        self.name = name
        self._item = None
        self.item = item
        self.settings = self.SETTINGS.copy()

    @property
    def artist(self):
        if not self._artist:
            self._artist = Artist(self.item)
        return self._artist

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item
        self._artist = Artist(item)

    @staticmethod
    def register(item_type, object_type, context=None):
        Object.ITEM_OBJECT[context][item_type] = object_type

    @abstractmethod
    def draw(self):
        raise NotImplementedError

    @property
    def DATASCHEMA(self):
        import schema
        return schema.Schema({
            'name': str,
            'item': Data,
            'settings': dict,
        })

    @property
    def JSONSCHEMANAME(self):
        return self.__class__.__name__

    @property
    def data(self):
        return {
            'name': self.name,
            'item': self.item,
            'settings': self.settings
        }

    @classmethod
    def from_data(cls, data):
        obj = cls(data['item'], name=data['name'])
        obj.settings = data['settings']
        return obj
