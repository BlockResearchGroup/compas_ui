from .value import Value
from compas.colors import Color

class ColorValue(Value):

    def __init__(self, value):
        value = Color(*value)
        super(ColorValue, self).__init__(value, Color)

    def cast(self, value):
        try:
            return Color(*value)
        except ValueError:
            raise ValueError("Cannot cast {} to {}".format(value, self.value_type))