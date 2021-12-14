from compas.plugins import pluggable


@pluggable(category='ui')
def get_real():
    raise NotImplementedError


class UserInterface(object):

    def __init__(self, app):
        self.app = app

    def get_real(self, *args, **kwargs):
        return get_real(*args, **kwargs)
