import compas

if compas.IPY:
    from .singleton_ipy import Singleton
else:
    from .singleton_py3 import Singleton

__all__ = ['Singleton']
