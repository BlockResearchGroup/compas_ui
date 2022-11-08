from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import uuid
from .object import Object
from compas_ui.values import Settings


class CurveObject(Object):

    SETTINGS = Settings()

    def __init__(self, *args, **kwargs):
        super(CurveObject, self).__init__(*args, **kwargs)

    @property
    def state(self):
        return {
            "guid": str(self.guid),
            "name": self.name,
            "item": str(self.item.guid),
            "parent": str(self.parent.guid) if self.parent else None,
            "settings": self.settings,
            "artist": self.artist.state,
            "visible": self.visible,
        }

    @state.setter
    def state(self, state):
        self._guid = uuid.UUID(state["guid"])
        self.name = state["name"]
        self.settings.update(state["settings"])
        self.artist.state = state["artists"]
        self.visible = state["visible"]

    @property
    def curve(self):
        return self.item

    @curve.setter
    def curve(self, curve):
        self.item = curve

    def move(self):
        raise NotImplementedError

    def move_start(self):
        raise NotImplementedError

    def move_end(self):
        raise NotImplementedError

    def move_knot(self):
        raise NotImplementedError
