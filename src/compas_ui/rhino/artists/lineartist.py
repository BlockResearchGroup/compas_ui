from compas_rhino.artists import LineArtist


class LineArtist(LineArtist):
    @property
    def state(self):
        return {
            "default_color": self.default_color,
            "color": self.color,
        }

    @state.setter
    def state(self, state):
        self.default_color = state['default_color']
        self.color = state['color']
