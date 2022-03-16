from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.app import App


__commandname__ = 'COMPAS_clear'


def RunCommand(is_interactive):

    compas_rhino.clear()

    app = App(name='COMPAS')
    app.session.reset()
    app.scene.clear()
    app.record()

    compas_rhino.redraw()


if __name__ == '__main__':
    RunCommand(True)
