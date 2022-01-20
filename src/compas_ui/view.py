from .camera import Camera  # noqa F401


class View(object):

    def __init__(self, app, camera=None):
        self.app = app
