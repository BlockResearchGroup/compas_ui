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


__all__ = [
    'ObjectNotRegistered',
    'Object',
    'MeshObject',
    'NetworkObject',
    'VolMeshObject'
]
