from compas_ui.artists import MeshArtist
from compas_rhino.artists import MeshArtist as BlenderMeshArtist


class MeshArtist(BlenderMeshArtist, MeshArtist):
    pass
