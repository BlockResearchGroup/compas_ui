from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from copy import deepcopy
from collections import deque

from compas.plugins import pluggable

from compas_ui.objects import Object
# from compas_ui.singleton import Singleton


@pluggable(category='ui')
def update_scene(self):
    raise NotImplementedError


@pluggable(category='ui')
def clear_scene(self):
    raise NotImplementedError


class Scene(object):

    def __init__(self, settings=None):
        super(Scene, self).__init__()
        self._history = deque()
        self._current = 0
        self.objects = []
        self.settings = settings or {}

    @property
    def data(self):
        return {'objects': self.objects, 'settings': self.settings}

    @data.setter
    def data(self, data):
        self.objects = data['objects']
        self.settings = data['settings']

    def record(self):
        if self._current != 0:
            self._history = deque(list(self._history)[self._current + 1:])
        self._history.appendleft(deepcopy(self.data))

    def undo(self):
        self.clear()
        if self._current == len(self._history) - 1:
            print("Nothing more to undo!")
            return
        self._current += 1
        self.data = self._history[self._current]
        self.update()

    def redo(self):
        self.clear()
        if self._current == 0:
            print("Nothing more to redo!")
            return
        self._current -= 1
        self.data = self._history[self._current]
        self.update()

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

    def update(self):
        update_scene(self)

    def clear(self):
        clear_scene(self)
