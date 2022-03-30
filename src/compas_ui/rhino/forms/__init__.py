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

    CondaEnvsForm
    ErrorForm
    FileForm
    MeshDataForm
    SearchPathsForm
    SettingsForm
    SceneObjectsForm
    SplashForm

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

from .conda import CondaEnvsForm
from .error import ErrorForm, error
from .files import FileForm
from .meshdata import MeshDataForm
from .searchpaths import SearchPathsForm
from .settings import SettingsForm
from .scene import SceneObjectsForm
from .splash import SplashForm


__all__ = [
    "CondaEnvsForm",
    "ErrorForm",
    "error",
    "FileForm",
    "MeshDataForm",
    "SearchPathsForm",
    "SettingsForm",
    "SceneObjectsForm",
    "SplashForm",
]
