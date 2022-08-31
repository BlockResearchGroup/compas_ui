from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.artists import CurveArtist
from compas_rhino.artists import CurveArtist as RhinoCurveArtist


class CurveArtist(RhinoCurveArtist, CurveArtist):
    pass
