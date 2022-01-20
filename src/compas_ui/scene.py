from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from uuid import uuid4
from compas.plugins import pluggable

from compas_ui.objects import Object


@pluggable(category='ui')
def update_scene(self):
    raise NotImplementedError


@pluggable(category='ui')
def clear_scene(self):
    raise NotImplementedError


class Scene(object):

    def __init__(self, app, settings={}):
        self.app = app
        self.nodes = {}
        self.settings = settings

    def add(self, item, **kwargs):
        if self.app.CONTEXT:
            kwargs['context'] = self.app.CONTEXT
        node = Object(item, **kwargs)
        guid = uuid4()
        self.nodes[guid] = node
        return node

    def get(self, name):
        selected = []
        for guid in self.nodes:
            if name == self.nodes[guid].name:
                selected.append(self.nodes[guid])
        if len(selected) == 0:
            return [None]
        else:
            return selected

    def update(self):
        update_scene(self)

    def clear(self):
        clear_scene(self)

    # def update_settings(self, settings=None):
    #     # should this not produce some kind of result we can react to?
    #     SettingsForm.from_settings(self.settings)

    # def clear_selection(self):
    #     compas_rhino.rs.UnselectAllObjects()

    # def update_selection(self, guids):
    #     compas_rhino.rs.SelectObjects(guids)

    # @property
    # def registered_object_types(self):
    #     return MeshObject.registered_object_types()
