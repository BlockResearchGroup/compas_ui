"""
********************************************************************************
blender.objects
********************************************************************************

.. currentmodule:: compas_ui.blender.objects

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BlenderMeshObject

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import plugin
from compas.datastructures import Mesh

from .object import BlenderObject
from .meshobject import BlenderMeshObject
from compas_ui.objects.group import Group
from compas_ui.objects.groupobject import GroupObject


@plugin(category="ui", requires=["bpy"])
def register_objects():
    BlenderObject.register(Mesh, BlenderMeshObject, context="Blender")
    BlenderObject.register(Group, GroupObject, context="Blender")

    print("UI Blender Objects registered.")


__all__ = [
    "BlenderObject",
    "BlenderMeshObject",
]
