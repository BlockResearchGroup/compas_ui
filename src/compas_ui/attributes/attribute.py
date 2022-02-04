from abc import abstractmethod


class Attribute(object):

    def __init__(self):
        raise NotImplementedError

    def __set_name__(self, owner, name):
        raise NotImplementedError

    def __get__(self, obj, objtype=None):
        raise NotImplementedError

    def __set__(self, obj, value):
        raise NotImplementedError

    @abstractmethod
    def initialize(self):
        raise NotImplementedError

    @abstractmethod
    def validate(self):
        raise NotImplementedError

    @abstractmethod
    def coerce(self):
        raise NotImplementedError

    @abstractmethod
    def ui(self):
        raise NotImplementedError
