from compas.colors import Color
from .attribute import Attribute
from .errors import ValidationError
from .errors import CoercionError


class ColorAttribute(Attribute):

    def __init__(self, color):
        self.type = Color
        self.value = self.validate(color)

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name) or self.value

    def __set__(self, obj, value):
        value = self.validate(value)
        setattr(obj, self.private_name, value)

    def validate(self, value):
        if not isinstance(value, self.type):
            try:
                value = self.coerce(value)
            except CoercionError:
                raise ValidationError("The provided value is not of type {}: {}".format(self.type, value))
        return value

    def coerce(self, value):
        try:
            value = Color.coerce(value)
        except Exception:
            raise CoercionError("the provided value could not be coerced into an instance of type {}: {}".format(self.type, value))
        return value

    def ui(self):
        pass
