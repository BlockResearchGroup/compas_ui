from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from uuid import uuid4
from compas.plugins import pluggable
from compas.data import Data
from compas_ui.objects import Object
from compas_ui.singleton import Singleton


@pluggable(category='ui')
def update_scene(self):
    raise NotImplementedError


@pluggable(category='ui')
def clear_scene(self):
    raise NotImplementedError


class Scene(Data, Singleton):

    def __init__(self, app=None, settings={}):
        self.app = app
        self.objects = set()
        self.settings = settings

    def add(self, item, **kwargs):
        node = Object(item, **kwargs)
        guid = str(uuid4())
        self.objects.add(guid)
        self.app.session['objects'][guid] = node
        return node

    def get(self, name):
        selected = []
        for guid in self.objects:
            obj = self.app.session['objects'][guid]
            if name == obj.name:
                selected.append(obj)
        if len(selected) == 0:
            return [None]
        else:
            return selected

    def update(self):
        update_scene(self)

    def clear(self):
        clear_scene(self)

    @property
    def DATASCHEMA(self):
        import schema
        return schema.Schema({
            'objects': list,
            'settings': dict,
        })

    @property
    def JSONSCHEMANAME(self):
        return self.__class__.__name__

    @property
    def data(self):
        return {
            'objects': list(self.objects),
            'settings': dict(self.settings)
        }

    @data.setter
    def data(self, data):
        self.clear()
        self.objects = set(data['objects'])
        self.settings = data['settings']
