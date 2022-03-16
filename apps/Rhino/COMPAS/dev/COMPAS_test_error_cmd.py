from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.app import App
from compas_ui.rhino.forms.error import error


__commandname__ = 'COMPAS_test_error'


@error()
def RunCommand(is_interactive):

    app = App(name='COMPAS')
    app.kaka


if __name__ == '__main__':
    RunCommand(True)
