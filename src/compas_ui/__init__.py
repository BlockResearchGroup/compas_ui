"""
********************************************************************************
compas_ui
********************************************************************************

.. currentmodule:: compas_ui


.. toctree::
    :maxdepth: 1

    compas_ui.app
    compas_ui.objects
    compas_ui.rhino
    compas_ui.scene
    compas_ui.session
    compas_ui.singleton


"""

from __future__ import print_function

import os


__author__ = ["tom van mele"]
__copyright__ = "ETH Zurich - Block Research Group"
__license__ = "MIT License"
__email__ = "van.mele@arch.ethz.ch"
__version__ = "0.8.4"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]

__all_plugins__ = [
    "compas_ui.rhino.objects",
    "compas_ui.rhino.artists",
    "compas_ui.rhino.scene",
    "compas_ui.rhino.install",
]
