from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.app import App


__commandname__ = 'COMPAS_test_undo'


def RunCommand(is_interactive):

    app = App(name='COMPAS')
    app.undo()


if __name__ == '__main__':
    RunCommand(True)
