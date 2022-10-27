from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import reduce
from operator import mul

from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import transform_points

from .object import Object
from compas_ui.values import Settings
from compas_ui.values import ColorValue
from compas_ui.values import BoolValue


class VolMeshObject(Object):
    """Class for representing COMPAS volmeshes in Rhino.

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

    SETTINGS = Settings(
        {
            "color.vertices": ColorValue((1, 1, 1)),
            "color.edges": ColorValue((0, 0, 0)),
            "color.faces": ColorValue((0.5, 0.5, 0.5)),
            "color.cells": ColorValue((1, 0, 0)),
            "show.vertices": BoolValue(True),
            "show.edges": BoolValue(True),
            "show.faces": BoolValue(True),
            "show.cells": BoolValue(False),
            "show.vertexlabels": BoolValue(False),
            "show.facelabels": BoolValue(False),
            "show.edgelabels": BoolValue(False),
            "show.celllabels": BoolValue(False),
        }
    )

    def __init__(self, *args, **kwargs):
        super(VolMeshObject, self).__init__(*args, **kwargs)
        self._anchor = None
        self._location = None
        self._scale = None
        self._rotation = None

    @property
    def volmesh(self):
        return self.item

    @volmesh.setter
    def volmesh(self, volmesh):
        self.item = volmesh

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, vertex):
        if self.volmesh.has_vertex(vertex):
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
            self._scale = 1.0
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
        vertices = list(self.volmesh.vertices())
        xyz = self.volmesh.vertices_attributes(["x", "y", "z"], keys=vertices)

        stack = []
        if self.scale != 1:
            S = Scale.from_factors([self.scale] * 3)
            stack.append(S)
        if self.rotation != [0, 0, 0]:
            R = Rotation.from_euler_angles(self.rotation)
            stack.append(R)
        if self.location != origin:
            if self.anchor is not None:
                xyz = self.volmesh.vertex_attributes(self.anchor, "xyz")
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

    def select_faces(self):
        raise NotImplementedError

    def select_edges(self):
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

    def move_face(self, face):
        raise NotImplementedError
