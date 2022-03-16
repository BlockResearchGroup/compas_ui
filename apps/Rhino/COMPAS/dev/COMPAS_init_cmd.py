from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from __plugin__ import settings

from compas_ui.app import App


__commandname__ = 'COMPAS_init'


def RunCommand(is_interactive):

    App._instances = {}

    app = App(name='COMPAS', settings=settings)
    app.scene.clear()


if __name__ == '__main__':
    RunCommand(True)
