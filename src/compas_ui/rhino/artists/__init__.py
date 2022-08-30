from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import plugin
from compas.artists import Artist

from compas.geometry import Line
from compas.datastructures import Mesh

from .lineartist import LineArtist
from .meshartist import MeshArtist


@plugin(category="factories", requires=["Rhino"])
def register_artists():
    Artist.register(Line, LineArtist, context="Rhino")
    Artist.register(Mesh, MeshArtist, context="Rhino")

    print("UI Rhino Artists registered.")


__all__ = [
    "LineArtist",
    "MeshArtist",
]
