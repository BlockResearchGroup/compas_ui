from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino
import Rhino.UI
import Rhino.Geometry

import compas_rhino

from compas.geometry import Point
from compas_rhino.conversions import vector_to_compas

from compas_ui.objects import MeshObject

from ._modify import mesh_update_attributes
from ._modify import mesh_update_vertex_attributes
from ._modify import mesh_update_face_attributes
from ._modify import mesh_update_edge_attributes
from ._modify import mesh_move_vertex
from ._modify import mesh_move_vertices

from .object import RhinoObject


class RhinoMeshObject(RhinoObject, MeshObject):
    """Class for representing COMPAS meshes in Rhino.

    Attributes
    ----------
    guid_vertex : dict[System.Guid, int]
        Map between Rhino object GUIDs and mesh vertex identifiers.
    guid_edge : dict[System.Guid, tuple[int, int]]
        Map between Rhino object GUIDs and mesh edge identifiers.
    guid_face : dict[System.Guid, int]
        Map between Rhino object GUIDs and mesh face identifiers.

    """

    def __init__(self, *args, **kwargs):
        super(RhinoMeshObject, self).__init__(*args, **kwargs)
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}

    @property
    def mesh(self):
        return self.item

    @mesh.setter
    def mesh(self, mesh):
        self.item = mesh
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}

    @property
    def guid_vertex(self):
        return self._guid_vertex

    @guid_vertex.setter
    def guid_vertex(self, values):
        self._guid_vertex = dict(values)

    @property
    def guid_edge(self):
        return self._guid_edge

    @guid_edge.setter
    def guid_edge(self, values):
        self._guid_edge = dict(values)

    @property
    def guid_face(self):
        return self._guid_face

    @guid_face.setter
    def guid_face(self, values):
        self._guid_face = dict(values)

    def clear(self):
        compas_rhino.delete_objects(self.guids, purge=True)
        self._guids = []
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}

    def draw(self):
        self.clear()
        if not self.visible:
            return
        self.artist.vertex_xyz = self.vertex_xyz

        if self.settings["show.vertices"]:
            vertices = list(self.mesh.vertices())
            guids = self.artist.draw_vertices(vertices=vertices, color=self.settings["color.vertices"])
            self.guids += guids
            self.guid_vertex = zip(guids, vertices)

            if self.settings["show.vertexlabels"]:
                text = {vertex: str(vertex) for vertex in vertices}
                self.guids += self.artist.draw_vertexlabels(text=text, color=self.settings["color.vertices"])

            if self.settings["show.vertexnormals"]:
                self.guids += self.artist.draw_vertexnormals(vertices=vertices, color=self.settings["color.vertices"])

        if self.settings["show.edges"]:
            edges = list(self.mesh.edges())
            guids = self.artist.draw_edges(edges=edges, color=self.settings["color.edges"])
            self.guids += guids
            self.guid_edge = zip(guids, edges)

            if self.settings["show.edgelabels"]:
                text = {edge: "{}-{}".format(*edge) for edge in edges}
                self.guids += self.artist.draw_edgelabels(text=text, color=self.settings["color.edges"])

        if self.settings["show.mesh"]:
            self.guids += self.artist.draw(color=self.settings["color.faces"], disjoint=True)

        elif self.settings["show.faces"]:
            faces = list(self.mesh.faces())
            guids = self.artist.draw_faces(faces=faces, color=self.settings["color.faces"])
            self.guids += guids
            self.guid_face = zip(guids, faces)

            if self.settings["show.facelabels"]:
                text = {face: str(face) for face in faces}
                self.guids += self.artist.draw_facelabels(text=text, color=self.settings["color.faces"])

            if self.settings["show.facenormals"]:
                self.guids += self.artist.draw_facenormals(faces=faces, color=self.settings["color.faces"])

    def select_vertex(self, message="Select one vertex."):
        """Select one vertex of the mesh.

        Parameters
        ----------
        message : str, optional
            A custom prompt message.

        Returns
        -------
        int
            A vertex identifier.

        """
        guid = compas_rhino.select_point(message=message)
        if guid and guid in self.guid_vertex:
            return self.guid_vertex[guid]

    def select_vertices(self, message="Select vertices."):
        """Select vertices of the mesh.

        Parameters
        ----------
        message : str, optional
            A custom prompt message.

        Returns
        -------
        list[int]
            A list of vertex identifiers.

        """
        guids = compas_rhino.select_points(message=message)
        vertices = [self.guid_vertex[guid] for guid in guids if guid in self.guid_vertex]
        return vertices

    def select_faces(self, message="Select faces."):
        """Select faces of the mesh.

        Parameters
        ----------
        message : str, optional
            A custom prompt message.

        Returns
        -------
        list[int]
            A list of face identifiers.

        """
        guids = compas_rhino.select_meshes(message=message)
        faces = [self.guid_face[guid] for guid in guids if guid in self.guid_face]
        return faces

    def select_edges(self, message="Select edges."):
        """Select edges of the mesh.

        Parameters
        ----------
        message : str, optional
            A custom prompt message.

        Returns
        -------
        list[tuple[int, int]]
            A list of edge identifiers.

        """
        guids = compas_rhino.select_lines(message=message)
        edges = [self.guid_edge[guid] for guid in guids if guid in self.guid_edge]
        return edges

    def modify(self):
        """Update the attributes of the mesh.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.

        """
        return mesh_update_attributes(self.mesh)

    def modify_vertices(self, vertices, names=None):
        """Update the attributes of selected vertices.

        Parameters
        ----------
        vertices : list[int]
            The vertices of the vertices of which the attributes should be updated.
        names : list[str], optional
            The names of the attributes that should be updated.
            Default is to update all available attributes.

        Returns
        -------
        bool
            True if the attributes were successfully updated.
            False otherwise.

        """
        return mesh_update_vertex_attributes(self.mesh, vertices, names=names)

    def modify_edges(self, edges, names=None):
        """Update the attributes of the edges.

        Parameters
        ----------
        edges : list[tuple[int, int]]
            The edges to update.
        names : list[str], optional
            The names of the atrtibutes to update.
            Default is to update all attributes.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.

        """
        return mesh_update_edge_attributes(self.mesh, edges, names=names)

    def modify_faces(self, faces, names=None):
        """Update the attributes of selected faces.

        Parameters
        ----------
        faces : list[int]
            The faces to update.
        names : list[str], optional
            The names of the attributes that should be updated.
            Default is to update all available attributes.

        Returns
        -------
        bool
            True if the attributes were successfully updated.
            False otherwise.

        """
        return mesh_update_face_attributes(self.mesh, faces, names=names)

    def move(self):
        """
        Move the entire mesh to a different location.

        Returns
        -------
        bool
            True if the operation was successful.
            False otherwise.

        Examples
        --------
        .. code-block:: python

            pass

        """
        mesh = self.mesh
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor

        vertex_p0 = {v: Rhino.Geometry.Point3d(*mesh.vertex_coordinates(v)) for v in mesh.vertices()}
        vertex_p1 = {v: Rhino.Geometry.Point3d(*mesh.vertex_coordinates(v)) for v in mesh.vertices()}

        edges = list(mesh.edges())

        def OnDynamicDraw(sender, e):
            current = e.CurrentPoint
            vector = current - start
            for vertex in vertex_p1:
                vertex_p1[vertex] = vertex_p0[vertex] + vector
            for u, v in iter(edges):
                sp = vertex[u]
                ep = vertex[v]
                e.Display.DrawDottedLine(sp, ep, color)

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt("Point to move from?")
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt("Point to move to?")
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()

        vector = vector_to_compas(end - start)
        for _, attr in mesh.vertices(True):
            attr["x"] += vector[0]
            attr["y"] += vector[1]
            attr["z"] += vector[2]
        return True

    def move_vertex(self, vertex):
        """Move a single vertex of the mesh object and update the data structure accordingly.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the operation was successful.
            False otherwise.

        """
        return mesh_move_vertex(self.mesh, vertex)

    def move_vertices(self, vertices):
        """Move a multiple vertices of the mesh object and update the data structure accordingly.

        Parameters
        ----------
        vertices : list[int]
            The identifiers of the vertices.

        Returns
        -------
        bool
            True if the operation was successful.
            False otherwise.

        """
        return mesh_move_vertices(self.mesh, vertices)

    def move_face(self, face):
        """Move a single face of the mesh object and update the data structure accordingly.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        bool
            True if the operation was successful.
            False otherwise.

        """
        raise NotImplementedError

    def move_vertices_direction(self, vertices, direction):
        """Move selected vertices along specified direction.

        Parameters
        ----------
        keys : list
            The identifiers of the vertices.
        direction: string, optional
            The name of axis or plane to move on. Defaut is the 'z'-axis.

        """

        def OnDynamicDraw(sender, e):
            draw = e.Display.DrawDottedLine
            end = e.CurrentPoint
            vector = end - start
            for a, b in lines:
                a = a + vector
                b = b + vector
                draw(a, b, color)
            for a, b in connectors:
                a = a + vector
                draw(a, b, color)

        mesh = self.mesh
        direction = direction.lower()
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        lines = []
        connectors = []

        for vertex in vertices:
            a = Rhino.Geometry.Point3d(*mesh.vertex_coordinates(vertex))
            nbrs = mesh.vertex_neighbors(vertex)
            for nbr in nbrs:
                b = Rhino.Geometry.Point3d(*mesh.vertex_coordinates(nbr))
                if nbr in vertices:
                    lines.append((a, b))
                else:
                    connectors.append((a, b))

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt("Point to move from?")
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()

        if direction == "x":
            geometry = Rhino.Geometry.Line(
                start,
                start + Rhino.Geometry.Vector3d(1, 0, 0),
            )
        elif direction == "y":
            geometry = Rhino.Geometry.Line(
                start,
                start + Rhino.Geometry.Vector3d(0, 1, 0),
            )
        elif direction == "z":
            geometry = Rhino.Geometry.Line(
                start,
                start + Rhino.Geometry.Vector3d(0, 0, 1),
            )
        elif direction == "xy":
            geometry = Rhino.Geometry.Plane(
                start,
                Rhino.Geometry.Vector3d(0, 0, 1),
            )
        elif direction == "yz":
            geometry = Rhino.Geometry.Plane(
                start,
                Rhino.Geometry.Vector3d(1, 0, 0),
            )
        elif direction == "zx":
            geometry = Rhino.Geometry.Plane(
                start,
                Rhino.Geometry.Vector3d(0, 1, 0),
            )

        gp.SetCommandPrompt("Point to move to?")
        gp.SetBasePoint(start, False)
        gp.DrawLineFromPoint(start, True)
        gp.DynamicDraw += OnDynamicDraw

        if direction in ("x", "y", "z"):
            gp.Constrain(geometry)
        else:
            gp.Constrain(geometry, False)

        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()
        vector = vector_to_compas(end - start)

        for vertex in vertices:
            point = Point(*mesh.vertex_attributes(vertex, "xyz"))
            mesh.vertex_attributes(vertex, "xyz", point + vector)

        return True
