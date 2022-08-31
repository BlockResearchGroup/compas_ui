from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import CurveArtist


class CurveArtist(CurveArtist):
    @property
    def state(self):
        return {
            "default_color": self.default_color,
            "color": self.color,
        }

    @state.setter
    def state(self, state):
        self.default_color = state["default_color"]
        self.color = state["color"]
