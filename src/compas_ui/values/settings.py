from .value import Value
from .dictvalue import DictValue


class Settings(DictValue):
    def __init__(self, settings):
        super(Settings, self).__init__(settings, Value)

    def __getitem__(self, key):
        return self.value[key].value

    def __setitem__(self, key, value):
        self.value[key].value = value

    def keys(self):
        return self.value.keys()
    
    def get(self, key, valueobject=False):
        if valueobject:
            return self.value[key]
        else:
            return self.value[key].value