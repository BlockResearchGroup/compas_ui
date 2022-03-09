from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# from collections import deque

from compas.plugins import pluggable
# from compas.data import json_load
# from compas.data import json_loads
# from compas.data import json_dump
# from compas.data import json_dumps
from compas_ui.objects import Object
from compas_ui.singleton import Singleton


@pluggable(category='ui')
def update_scene(self):
    raise NotImplementedError


@pluggable(category='ui')
def clear_scene(self):
    raise NotImplementedError


class Scene(Singleton):

    def __init__(self, settings=None):
        self.objects = []
        self.settings = settings or {}

    def add(self, item, **kwargs):
        obj = Object(item, scene=self, **kwargs)
        # implement __hash__ on Data
        # to allow for
        # self.objects[item] = obj
        self.objects.append(obj)
        return obj

    def get(self, name):
        objects = []
        for obj in self.objects:
            if name == obj.name:
                objects.append(obj)
        return objects

    # @property
    # def snapshot(self):
    #     objdata = []
    #     for obj in self.objects:
    #         objdata.append(obj.data)
    #     return json_dumps(objdata)

    # @snapshot.setter
    # def snapshot(self, snapshot):
    #     self.data = json_loads(snapshot)

    # def record(self):
    #     if self._current != 0:
    #         self._history = deque(list(self._history)[self._current + 1:])
    #     self._history.appendleft(self.snapshot)

    def update(self):
        update_scene(self)

    def clear(self):
        clear_scene(self)
