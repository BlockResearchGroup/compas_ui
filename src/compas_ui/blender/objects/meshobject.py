import compas_blender

from compas_ui.objects import MeshObject
from .object import BlenderObject


class BlenderMeshObject(BlenderObject, MeshObject):
    """Class for representing COMPAS meshes in Blender."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._object_vertex = {}
        self._object_edge = {}
        self._object_face = {}

    @property
    def mesh(self):
        return self.item

    @mesh.setter
    def mesh(self, mesh):
        self.item = mesh
        self._object_vertex = {}
        self._object_edge = {}
        self._object_face = {}

    @property
    def object_vertex(self):
        return self._object_vertex

    @object_vertex.setter
    def object_vertex(self, values):
        self._object_vertex = dict(values)

    @property
    def object_edge(self):
        return self._object_edge

    @object_edge.setter
    def object_edge(self, values):
        self._object_edge = dict(values)

    @property
    def object_face(self):
        return self._object_face

    @object_face.setter
    def object_face(self, values):
        self._object_face = dict(values)

    def clear(self):
        compas_blender.delete_objects(self.objects, purge_data=True)
        self._objects = []
        self._object_vertex = {}
        self._object_edge = {}
        self._object_face = {}

    def draw(self):
        self.clear()
        if not self.visible:
            return
        self.artist.vertex_xyz = self.vertex_xyz

        if self.settings["show.vertices"]:
            vertices = list(self.mesh.vertices())
            objects = self.artist.draw_vertices(
                vertices=vertices, color=self.settings["color.vertices"]
            )
            self.objects += objects
            self.object_vertex = zip(objects, vertices)

            if self.settings["show.vertexlabels"]:
                raise NotImplementedError

            if self.settings["show.vertexnormals"]:
                self.objects += self.artist.draw_vertexnormals(
                    vertices=vertices, color=self.settings["color.vertices"]
                )

        if self.settings["show.edges"]:
            edges = list(self.mesh.edges())
            objects = self.artist.draw_edges(
                edges=edges, color=self.settings["color.edges"]
            )
            self.objects += objects
            self.object_edge = zip(objects, edges)

            if self.settings["show.edgelabels"]:
                raise NotImplementedError

        if self.settings["show.mesh"]:
            self.objects += self.artist.draw(color=self.settings["color.faces"])

        elif self.settings["show.faces"]:
            faces = list(self.mesh.faces())
            objects = self.artist.draw_faces(
                faces=faces, color=self.settings["color.faces"]
            )
            self.objects += objects
            self.object_face = zip(objects, faces)

            if self.settings["show.facelabels"]:
                raise NotImplementedError

            if self.settings["show.facenormals"]:
                self.objects += self.artist.draw_facenormals(
                    faces=faces, color=self.settings["color.faces"]
                )
