from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import uuid
from functools import reduce
from operator import mul

from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import transform_points
from compas.colors import Color
from compas_ui.values import Settings
from compas_ui.values import ColorValue
from compas_ui.values import BoolValue

from .object import Object

# TODO: color settings should be on the artist
# TODO: provide form for evey scene object with separate pages for scene settings, artist settings, data, ...
# TODO: remove the transformations and view coordinates? (specific to form/force diagram context)


class MeshObject(Object):
    """Base class for all scene objects representing meshes.

    Attributes
    ----------
    anchor : int
        The vertex of the mesh that is anchored to the location of the object.
    location : :class:`compas.geometry.Point`
        The location of the object.
        Default is the origin of the world coordinate system.
    scale : float
        A uniform scaling factor for the object in the scene.
        The scale is applied relative to the location of the object in the scene.
    rotation : list[float]
        The rotation angles around the 3 axis of the coordinate system
        with the origin placed at the location of the object in the scene.
    vertex_xyz : dict[int, list[float]]
        The view coordinates of the mesh object.

    """

    # the color settings duplicate the colors settings of the artist
    SETTINGS = Settings(
        {
            "color.vertices": ColorValue(Color.from_hex("#0092d2")),
            "color.edges": ColorValue(Color.from_hex("#0092d2")),
            "color.faces": ColorValue(Color.from_hex("#0092d2").lightened(50)),
            "show.mesh": BoolValue(True),
            "show.vertices": BoolValue(False),
            "show.edges": BoolValue(False),
            "show.faces": BoolValue(False),
            "show.vertexlabels": BoolValue(False),
            "show.facelabels": BoolValue(False),
            "show.edgelabels": BoolValue(False),
            "show.vertexnormals": BoolValue(False),
            "show.facenormals": BoolValue(False),
        }
    )

    def __init__(self, *args, **kwargs):
        super(MeshObject, self).__init__(*args, **kwargs)
        self._anchor = None
        self._location = None
        self._scale = None
        self._rotation = None

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
            "anchor": self.anchor,
            "location": self.location,
            "scale": self.scale,
            "rotation": self.rotation,
        }

    @state.setter
    def state(self, state):
        self._guid = uuid.UUID(state["guid"])
        self.name = state["name"]
        self.settings.update(state["settings"])
        self.artist.state = state["artists"]
        self.visible = state["visible"]
        # parent?
        # item?
        self.anchor = state["anchor"]
        self.location = state["location"]
        self.scale = state["scale"]
        self.rotation = state["rotation"]

    @property
    def mesh(self):
        return self.item

    @mesh.setter
    def mesh(self, mesh):
        self.item = mesh

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, vertex):
        if self.mesh.has_vertex(vertex):
            self._anchor = vertex

    @property
    def location(self):
        if not self._location:
            self._location = Point(0, 0, 0)
        return self._location

    @location.setter
    def location(self, location):
        self._location = Point(*location)

    @property
    def scale(self):
        if not self._scale:
            self._scale = 1
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale

    @property
    def rotation(self):
        if not self._rotation:
            self._rotation = [0, 0, 0]
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = rotation

    @property
    def vertex_xyz(self):
        origin = Point(0, 0, 0)
        vertices = list(self.mesh.vertices())
        xyz = self.mesh.vertices_attributes(["x", "y", "z"], keys=vertices)

        stack = []
        if self.scale != 1:
            S = Scale.from_factors([self.scale] * 3)
            stack.append(S)
        if self.rotation != [0, 0, 0]:
            R = Rotation.from_euler_angles(self.rotation)
            stack.append(R)
        if self.location != origin:
            if self.anchor is not None:
                xyz = self.mesh.vertex_attributes(self.anchor, "xyz")
                point = Point(*xyz)
                T1 = Translation.from_vector(origin - point)
                stack.insert(0, T1)
            T2 = Translation.from_vector(self.location)
            stack.append(T2)

        if stack:
            X = reduce(mul, stack[::-1])
            xyz = transform_points(xyz, X)
        return dict(zip(vertices, xyz))

    def select_vertex(self):
        raise NotImplementedError

    def select_vertices(self):
        raise NotImplementedError

    def select_edge(self):
        raise NotImplementedError

    def select_edges(self):
        raise NotImplementedError

    def select_face(self):
        raise NotImplementedError

    def select_faces(self):
        raise NotImplementedError

    def modify_vertices(self, vertices, names=None):
        raise NotImplementedError

    def modify_edges(self, edges, names=None):
        raise NotImplementedError

    def modify_faces(self, faces, names=None):
        raise NotImplementedError

    def move_vertex(self, vertex):
        raise NotImplementedError

    def move_vertices(self, vertices):
        raise NotImplementedError

    def move_edge(self, edge):
        raise NotImplementedError

    def move_face(self, face):
        raise NotImplementedError
