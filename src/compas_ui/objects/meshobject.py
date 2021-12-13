from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.artists import Artist
from .object import Object


class MeshObject(Object):

    def __init__(self, item, *args, **kwargs):
        self._artist = None
        self._item = None
        self.item = item
        self.guids = None

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

    def draw(self):
        self.guids = self.artist.draw()

    def clear(self):
        pass

    def select_vertex(self):
        pass

    def select_vertices(self):
        pass

    def select_edge(self):
        pass

    def select_edges(self):
        pass

    def select_face(self):
        pass

    def select_faces(self):
        pass
