from .value import Value


class FloatValue(Value):
    def __init__(self, value=0.0, min=None, max=None, options=None):
        super(FloatValue, self).__init__(value, float, options=options)
        if min is not None:
            self._check_type(min)
        if max is not None:
            self._check_type(max)
        self._min = min
        self._max = max
        self._check_bounds(value)

    def _check_bounds(self, value):
        if self.min is not None:
            assert value >= self.min, "Value must be greater than {}".format(self.min)
        if self.max is not None:
            assert value <= self.max, "Value must be less than {}".format(self.max)

    def check(self, value):
        super(FloatValue, self).check(value)
        self._check_bounds(value)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        self._check_type(value)
        self._min = value

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        self._check_type(value)
        self._max = value

    @property
    def data(self):
        return {
            "value": self.value,
            "value_type": "float",
            "options": self.options,
            "min": self.min,
            "max": self.max,
        }

    @data.setter
    def data(self, data):
        self._value = data["value"]
        self._options = data["options"]
        self._min = data["min"]
        self._max = data["max"]
