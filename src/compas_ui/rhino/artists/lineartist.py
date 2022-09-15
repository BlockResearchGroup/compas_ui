from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.colors import Color
from compas_ui.artists import PrimitiveArtist
from compas_rhino.artists import LineArtist


class LineArtist(LineArtist, PrimitiveArtist):
    def draw(self, color=None, show_points=False):
        start = list(self.line.start)
        end = list(self.line.end)
        color = Color.coerce(color) or self.color
        color = color.rgb255
        guids = []
        if show_points:
            points = [
                {'pos': start, 'color': color, 'name': self.primitive.name},
                {'pos': end, 'color': color, 'name': self.primitive.name}
            ]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        lines = [{'start': start, 'end': end, 'color': color, 'name': self.primitive.name}]
        guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        return guids
