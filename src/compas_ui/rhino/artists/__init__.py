from compas.plugins import plugin
from compas.artists import Artist
from compas.datastructures import Mesh

from .meshartist import MeshArtist


@plugin(category="factories", requires=["Rhino"])
def register_artists():
    Artist.register(Mesh, MeshArtist, context="Rhino")
