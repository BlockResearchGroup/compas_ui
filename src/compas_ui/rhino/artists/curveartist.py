from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.artists import CurveArtist
from compas_rhino.artists import CurveArtist as RhinoCurveArtist
from compas.colors import Color


class CurveArtist(RhinoCurveArtist, CurveArtist):
    def draw(self, color=None):
        color = Color.coerce(color) or self.color
        curves = [{'curve': self.curve_transformed, 'color': color.rgb255, 'name': self.curve.name}]
        return compas_rhino.draw_curves(curves, layer=self.layer, clear=False, redraw=False)
