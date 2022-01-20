
from compas.artists import Artist

from compas.datastructures import Mesh
from .meshartist import MeshArtist

Artist.register(Mesh, MeshArtist, context='Web')
