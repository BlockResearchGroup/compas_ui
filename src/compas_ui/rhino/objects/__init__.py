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

    RhinoCurveObject
    RhinoLineObject
    RhinoMeshObject
    RhinoNetworkObject
    RhinoVolMeshObject

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import plugin
from compas.geometry import Curve
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
)

from .object import RhinoObject
from .curveobject import RhinoCurveObject
from .lineobject import RhinoLineObject
from .meshobject import RhinoMeshObject
from .networkobject import RhinoNetworkObject
from .volmeshobject import RhinoVolMeshObject
from compas_ui.objects.group import Group
from compas_ui.objects.groupobject import GroupObject


@plugin(category="ui", requires=["Rhino"])
def register_objects():
    RhinoObject.register(Curve, RhinoCurveObject, context="Rhino")
    RhinoObject.register(Line, RhinoLineObject, context="Rhino")
    RhinoObject.register(Mesh, RhinoMeshObject, context="Rhino")
    RhinoObject.register(Network, RhinoNetworkObject, context="Rhino")
    RhinoObject.register(VolMesh, RhinoVolMeshObject, context="Rhino")
    RhinoObject.register(Group, GroupObject, context="Rhino")

    print("UI Rhino Objects registered.")


__all__ = [
    "RhinoObject",
    "RhinoCurveObject",
    "RhinoLineObject",
    "RhinoMeshObject",
    "RhinoNetworkObject",
    "RhinoVolMeshObject",
]
