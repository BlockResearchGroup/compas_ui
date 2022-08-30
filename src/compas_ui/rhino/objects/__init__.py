"""
********************************************************************************
rhino.objects
********************************************************************************

.. currentmodule:: compas_ui.rhino.objects

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RhinoLineObject
    RhinoMeshObject
    RhinoNetworkObject
    RhinoVolMeshObject

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import plugin
from compas.geometry import Line
from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

from ._modify import (  # noqa : F401 F403
    network_update_attributes,
    network_update_node_attributes,
    network_update_edge_attributes,
    network_move_node,
    mesh_update_attributes,
    mesh_update_vertex_attributes,
    mesh_update_face_attributes,
    mesh_update_edge_attributes,
    mesh_move_vertex,
    mesh_move_vertices,
    mesh_move_face,
)

from .object import RhinoObject
from .lineobject import RhinoLineObject
from .meshobject import RhinoMeshObject
from .networkobject import RhinoNetworkObject
from .volmeshobject import RhinoVolMeshObject


@plugin(category='ui', requires=["Rhino"])
def register_objects():
    RhinoObject.register(Line, RhinoLineObject, context="Rhino")
    RhinoObject.register(Mesh, RhinoMeshObject, context="Rhino")
    RhinoObject.register(Network, RhinoNetworkObject, context="Rhino")
    RhinoObject.register(VolMesh, RhinoVolMeshObject, context="Rhino")

    print("UI Rhino Objects registered.")


__all__ = [
    "RhinoObject",
    "RhinoLineObject",
    "RhinoMeshObject",
    "RhinoNetworkObject",
    "RhinoVolMeshObject",
]
