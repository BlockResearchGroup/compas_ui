from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.artists import MeshArtist
from compas_rhino.artists import MeshArtist as RhinoMeshArtist


class MeshArtist(RhinoMeshArtist, MeshArtist):
    pass
