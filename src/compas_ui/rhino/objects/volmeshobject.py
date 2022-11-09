from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino

from compas_ui.objects import VolMeshObject

from ._modify import mesh_update_attributes
from ._modify import mesh_update_vertex_attributes
from ._modify import mesh_update_face_attributes
from ._modify import mesh_update_edge_attributes
from ._modify import mesh_move_vertex
from ._modify import mesh_move_vertices

from .object import RhinoObject


class RhinoVolMeshObject(RhinoObject, VolMeshObject):
    """Class for representing COMPAS volmeshes in Rhino.

    Attributes
    ----------
    guid_vertex : dict[System.Guid, int]
        Map between Rhino object GUIDs and volmesh vertex identifiers.
    guid_edge : dict[System.Guid, tuple[int, int]]
        Map between Rhino object GUIDs and volmesh edge identifiers.
    guid_face : dict[System.Guid, int]
        Map between Rhino object GUIDs and volmesh face identifiers.
    guid_cell : dict[System.Guid, int]
        Map between Rhino object GUIDs and volmesh cell identifiers.

    """

    def __init__(self, *args, **kwargs):
        super(RhinoVolMeshObject, self).__init__(*args, **kwargs)
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_cell = {}

    @property
    def volmesh(self):
        return self.item

    @volmesh.setter
    def volmesh(self, volmesh):
        self.item = volmesh
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_cell = {}

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

    @property
    def guid_cell(self):
        return self._guid_cell

    @guid_cell.setter
    def guid_cell(self, values):
        self._guid_cell = dict(values)

    def clear(self):
        """Clear all objects previously drawn by this artist."""
        compas_rhino.delete_objects(self.guids, purge=True)
        self._guids = []
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_cell = {}

    def draw(self):
        """Draw the volmesh using the visualisation settings."""
        self.clear()
        if not self.visible:
            return
        self.artist.vertex_xyz = self.vertex_xyz

        if self.settings["show.vertices"]:
            vertices = list(self.volmesh.vertices())
            guids = self.artist.draw_vertices(vertices=vertices, color=self.settings["color.vertices"])
            self.guids += guids
            self.guid_vertex = zip(guids, vertices)

            if self.settings["show.vertexlabels"]:
                text = {vertex: str(vertex) for vertex in vertices}
                self.guids += self.artist.draw_vertexlabels(text=text, color=self.settings["color.vertices"])

        if self.settings["show.faces"]:
            faces = list(self.volmesh.faces())
            guids = self.artist.draw_faces(faces=faces, color=self.settings["color.faces"])
            self.guids += guids
            self.guid_face = zip(guids, faces)

            if self.settings["show.facelabels"]:
                text = {face: str(face) for face in faces}
                self.guids += self.artist.draw_facelabels(text=text, color=self.settings["color.faces"])

        if self.settings["show.edges"]:
            edges = list(self.volmesh.edges())
            guids = self.artist.draw_edges(edges=edges, color=self.settings["color.edges"])
            self.guids += guids
            self.guid_edge = zip(guids, edges)

            if self.settings["show.edgelabels"]:
                text = {edge: "{}-{}".format(*edge) for edge in edges}
                self.guids += self.artist.draw_edgelabels(text=text, color=self.settings["color.edges"])

        if self.settings["show.cells"]:
            cells = list(self.volmesh.cells())
            guids = self.artist.draw_cells(cells=cells, color=self.settings["color.cells"])
            self.guids += guids
            self.guid_cell = zip(guids, cells)

            if self.settings["show.celllabels"]:
                text = {cell: str(cell) for cell in cells}
                self.guids += self.artist.draw_celllabels(text=text, color=self.settings["color.cells"])

    def select_vertex(self, message="Select one vertex."):
        """Select one vertex of the mesh.

        Returns
        -------
        int
            A vertex identifier.
        """
        guid = compas_rhino.select_point(message=message)
        if guid and guid in self.guid_vertex:
            return self.guid_vertex[guid]

    def select_vertices(self, message="Select vertices."):
        """Select vertices of the volmesh.

        Returns
        -------
        list
            A list of vertex identifiers.
        """
        guids = compas_rhino.select_points(message=message)
        vertices = [self.guid_vertex[guid] for guid in guids if guid in self.guid_vertex]
        return vertices

    def select_faces(self, message="Select faces."):
        """Select faces of the volmesh.

        Returns
        -------
        list
            A list of face identifiers.
        """
        guids = compas_rhino.select_meshes(message=message)
        faces = [self.guid_face[guid] for guid in guids if guid in self.guid_face]
        return faces

    def select_edges(self, message="Select edges."):
        """Select edges of the volmesh.

        Returns
        -------
        list
            A list of edge identifiers.
        """
        guids = compas_rhino.select_lines(message=message)
        edges = [self.guid_edge[guid] for guid in guids if guid in self.guid_edge]
        return edges

    def modify(self):
        """Update the attributes of the volmesh.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.
        """
        return mesh_update_attributes(self.volmesh)

    def modify_vertices(self, vertices, names=None):
        """Update the attributes of selected vertices.

        Parameters
        ----------
        vertices : list
            The vertices of the vertices of which the attributes should be updated.
        names : list, optional
            The names of the attributes that should be updated.
            Default is to update all available attributes.

        Returns
        -------
        bool
            True if the attributes were successfully updated.
            False otherwise.

        """
        return mesh_update_vertex_attributes(self.volmesh, vertices, names=names)

    def modify_edges(self, edges, names=None):
        """Update the attributes of the edges.

        Parameters
        ----------
        edges : list
            The edges to update.
        names : list, optional
            The names of the atrtibutes to update.
            Default is to update all attributes.

        Returns
        -------
        bool
            True if the update was successful.
            False otherwise.

        """
        return mesh_update_edge_attributes(self.volmesh, edges, names=names)

    def modify_faces(self, faces, names=None):
        """Update the attributes of selected faces.

        Parameters
        ----------
        vertices : list
            The vertices of the vertices of which the attributes should be updated.
        names : list, optional
            The names of the attributes that should be updated.
            Default is to update all available attributes.

        Returns
        -------
        bool
            True if the attributes were successfully updated.
            False otherwise.

        """
        return mesh_update_face_attributes(self.volmesh, faces, names=names)

    def move_vertex(self, vertex):
        """Move a single vertex of the volmesh object and update the data structure accordingly.

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
        return mesh_move_vertex(self.volmesh, vertex)

    def move_vertices(self, vertices):
        """Move a multiple vertices of the volmesh object and update the data structure accordingly.

        Parameters
        ----------
        vertices : list of int
            The identifiers of the vertices.

        Returns
        -------
        bool
            True if the operation was successful.
            False otherwise.
        """
        return mesh_move_vertices(self.volmesh, vertices)

    def move_face(self, face):
        """Move a single face of the volmesh object and update the data structure accordingly.

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
