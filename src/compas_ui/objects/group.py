from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .object import Object

class Group(Object):
    def __init__(self, items, **kwargs):
        super(Group, self).__init__(items, **kwargs)
        for item in items:
            self.add(item)

    def clear(self):
        for child in self.children:
            self.remove(child)

    def draw(self):
        pass