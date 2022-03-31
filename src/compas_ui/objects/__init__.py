"""
********************************************************************************
objects
********************************************************************************

.. currentmodule:: compas_ui.objects


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Object
    MeshObject
    NetworkObject
    VolMeshObject


Exceptions
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ObjectNotRegistered

"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .exceptions import ObjectNotRegistered
from .object import Object
from .meshobject import MeshObject
from .networkobject import NetworkObject
from .volmeshobject import VolMeshObject

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

from compas.plugins import plugin

@plugin(category="ui")
def register_objects():
    Object.register(Mesh, MeshObject, context=None)
    Object.register(Network, NetworkObject, context=None)
    Object.register(VolMesh, VolMeshObject, context=None)


__all__ = [
    'ObjectNotRegistered',
    'Object',
    'MeshObject',
    'NetworkObject',
    'VolMeshObject'
]
