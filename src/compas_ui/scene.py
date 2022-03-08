from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import pluggable
from compas_ui.objects import Object
from compas_ui.singleton import Singleton


@pluggable(category='ui')
def update_scene(self):
    raise NotImplementedError


@pluggable(category='ui')
def clear_scene(self):
    raise NotImplementedError


class Scene(Singleton):

    def __init__(self, app, settings=None):
        self.app = app
        self.objects = {}
        self.settings = settings or {}

    @property
    def data(self):
        return {
            'objects': self.objects,
            'settings': self.settings,
        }

    # this should re-assign the object ids
    # and reconstruct them to UUID objects
    @data.setter
    def data(self, data):
        self.clear()
        self.objects = data['objects']
        self.settings = data['settings']

    def add(self, item, **kwargs):
        obj = Object(item, scene=self, **kwargs)
        self.objects[str(obj.id)] = obj
        return obj

    def get(self, name):
        selected = []
        for id in self.objects:
            obj = self.objects[id]
            if name == obj.name:
                selected.append(obj)
        # why not just return the empty list?
        if len(selected) == 0:
            return [None]
        return selected

    def update(self):
        update_scene(self)

    def clear(self):
        clear_scene(self)
