"""
********************************************************************************
rhino
********************************************************************************

.. currentmodule:: compas_ui.rhino

Objects
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RhinoMeshObject
    RhinoNetworkObject
    RhinoVolMeshObject

Forms
=====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BrowserForm
    ErrorForm
    SettingsForm

Decorators
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    error


"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import plugin

from .install import installable_rhino_packages  # noqa : F401
from .scene import clear_scene  # noqa : F401
from .scene import update_scene  # noqa : F401

from .objects._modify import (  # noqa : F401 F403
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

from .objects._object import RhinoObject
from .objects.meshobject import RhinoMeshObject
from .objects.networkobject import RhinoNetworkObject
from .objects.volmeshobject import RhinoVolMeshObject

from .forms.browser import BrowserForm
from .forms.error import ErrorForm
from .forms.settings import SettingsForm

from .forms.error import error

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh


@plugin(category="ui", requires=["Rhino"])
def register_objects():
    RhinoObject.register(Mesh, RhinoMeshObject, context="Rhino")
    RhinoObject.register(Network, RhinoNetworkObject, context="Rhino")
    RhinoObject.register(VolMesh, RhinoVolMeshObject, context="Rhino")
    print("Rhino Objects registered.")


__all__ = [
    "RhinoObject",
    "RhinoMeshObject",
    "RhinoNetworkObject",
    "RhinoVolMeshObject",
    "BrowserForm",
    "ErrorForm",
    "SettingsForm",
    "error",
]
