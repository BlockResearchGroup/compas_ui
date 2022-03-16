"""
********************************************************************************
objects
********************************************************************************

.. currentmodule:: compas_ui.rhino.objects

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RhinoMeshObject
    RhinoNetworkObject
    RhinoVolMeshObject

"""
from __future__ import absolute_import

from compas.plugins import plugin

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
    mesh_move_face
)

from ._object import RhinoObject
from .meshobject import RhinoMeshObject
from .networkobject import RhinoNetworkObject
from .volmeshobject import RhinoVolMeshObject

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh


@plugin(category='ui', requires=['Rhino'])
def register_objects():
    RhinoObject.register(Mesh, RhinoMeshObject, context='Rhino')
    RhinoObject.register(Network, RhinoNetworkObject, context='Rhino')
    RhinoObject.register(VolMesh, RhinoVolMeshObject, context='Rhino')
    print('Rhino Objects registered.')


__all__ = [
    'RhinoObject',
    'RhinoMeshObject',
    'RhinoNetworkObject',
    'RhinoVolMeshObject'
]
