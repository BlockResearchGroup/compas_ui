from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Mesh

from .exceptions import DataObjectNotRegistered
from .object import Object
from .meshobject import MeshObject

Object.register(Mesh, MeshObject, context='Rhino')
Object.register(Mesh, MeshObject, context='Web')


__all__ = [
    'DataObjectNotRegistered',
    'Object',
    'MeshObject'
]
