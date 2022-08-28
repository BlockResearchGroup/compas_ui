from compas_rhino.artists import MeshArtist


class MeshArtist(MeshArtist):
    @property
    def state(self):
        return {
            "default_vertexcolor": self.default_vertexcolor,
            "default_edgecolor": self.default_edgecolor,
            "default_facecolor": self.default_facecolor,
            "_vertex_color": self._vertex_color,
            "_edge_color": self._edge_color,
            "_face_color": self._face_color,
            "vertices": self.vertices,
            "edges": self.edges,
            "faces": self.faces,
        }

    @state.setter
    def state(self, state):
        self.default_vertexcolor = state["default_vertexcolor"]
        self.default_edgecolor = state["default_edgecolor"]
        self.default_facecolor = state["default_facecolor"]
        self._vertex_color = state["_vertex_color"]
        self._edge_color = state["_edge_color"]
        self._face_color = state["_face_color"]
        self.vertices = state["vertices"]
        self.edges = state["edges"]
        self.faces = state["faces"]
