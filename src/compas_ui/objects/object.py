from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
from abc import abstractmethod
from collections import defaultdict

import compas
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


class Object(object):
    """Base class for all objects.
    """

    __OBJECTS_REGISTERED = False

    AVAILABLE_CONTEXTS = ['Rhino', 'Blender', 'Viewer']
    CONTEXT = None
    ITEM_OBJECT = defaultdict(dict)

    def __new__(cls, *args, **kwargs):
        if not Object.__OBJECTS_REGISTERED:
            register_objects()
            Object.__OBJECTS_REGISTERED = True
        cls = _get_object_cls(args[0], **kwargs)
        PluginValidator.ensure_implementations(cls)
        return super(Object, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        super(Object, self).__init__()
        self._ids = []

    @staticmethod
    def register(item_type, object_type, context=None):
        Object.ITEM_OBJECT[context][item_type] = object_type

    @abstractmethod
    def draw(self):
        raise NotImplementedError
