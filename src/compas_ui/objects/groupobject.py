from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .object import Object
import uuid


class GroupObject(Object):
    def __init__(self, group, **kwargs):
        super(GroupObject, self).__init__(group, **kwargs)
        for item in group.items:
            self.add(item)

    def clear(self):
        for child in self.children:
            self.remove(child)

    def draw(self):
        pass

    @property
    def state(self):
        return {
            "guid": str(self.guid),
            "name": self.name,
            "item": str(self.item.guid),
            "parent": str(self.parent.guid) if self.parent else None,
            "settings": self.settings,
            "visible": self.visible,
        }

    @state.setter
    def state(self, state):
        self._guid = uuid.UUID(state["guid"])
        self.name = state["name"]
        self.settings.update(state["settings"])
        self.visible = state["visible"]
