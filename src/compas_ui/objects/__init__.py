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
    CurveObject
    LineObject
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

from .lineobject import LineObject
from .curveobject import CurveObject
from .meshobject import MeshObject
from .networkobject import NetworkObject
from .volmeshobject import VolMeshObject
from .group import Group


__all__ = [
    "ObjectNotRegistered",
    "Object",
    "CurveObject",
    "LineObject",
    "MeshObject",
    "NetworkObject",
    "VolMeshObject",
    "Group",
]
