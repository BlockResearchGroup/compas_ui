"""
********************************************************************************
rhino.forms
********************************************************************************

.. currentmodule:: compas_ui.rhino.forms

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BrowserForm
    ErrorForm
    SettingsForm
    MeshForm

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

from .browser import BrowserForm
from .error import ErrorForm
from .settings import SettingsForm
from .error import error
from .mesh import MeshForm


__all__ = [
    "BrowserForm",
    "ErrorForm",
    "SettingsForm",
    "MeshForm",
    "error",
]
