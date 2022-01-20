from compas.artists import MeshArtist
from compas_ui.app import App


class MeshArtist(MeshArtist):

    def __init__(self, *args, **kwargs):
        super(MeshArtist, self).__init__(*args, **kwargs)
        self.webapp = App('').webapp

    def draw(self):
        self.webapp.draw(self.mesh.data)

    def draw_vertices(self, vertices=None, color=None, text=None):
        """Draw the vertices of the mesh.

        Parameters
        ----------
        vertices : list, optional
            The vertices to include in the drawing.
            Default is all vertices.
        color : tuple or dict, optional
            The color of the vertices,
            as either a single color to be applied to all vertices,
            or a color dict, mapping specific vertices to specific colors.
        text : dict, optional
            The text labels for the vertices
            as a text dict, mapping specific vertices to specific text labels.
        """
        raise NotImplementedError

    def draw_edges(self, edges=None, color=None, text=None):
        """Draw the edges of the mesh.

        Parameters
        ----------
        edges : list, optional
            The edges to include in the drawing.
            Default is all edges.
        color : tuple or dict, optional
            The color of the edges,
            as either a single color to be applied to all edges,
            or a color dict, mapping specific edges to specific colors.
        text : dict, optional
            The text labels for the edges
            as a text dict, mapping specific edges to specific text labels.
        """
        raise NotImplementedError

    def draw_faces(self, faces=None, color=None, text=None):
        """Draw the faces of the mesh.

        Parameters
        ----------
        faces : list, optional
            The faces to include in the drawing.
            Default is all faces.
        color : tuple or dict, optional
            The color of the faces,
            as either a single color to be applied to all faces,
            or a color dict, mapping specific faces to specific colors.
        text : dict, optional
            The text labels for the faces
            as a text dict, mapping specific faces to specific text labels.
        """
        raise NotImplementedError

    def draw_mesh(self):
        raise NotImplementedError

    def clear_vertices(self):
        raise NotImplementedError

    def clear_edges(self):
        raise NotImplementedError

    def clear_faces(self):
        raise NotImplementedError
