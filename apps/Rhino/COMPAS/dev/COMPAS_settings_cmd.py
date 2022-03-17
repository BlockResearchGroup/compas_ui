from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.app import App
from compas_ui.rhino import error


__commandname__ = 'COMPAS_settings'


@error()
def RunCommand(is_interactive):

    app = App()
    app.update_settings()


if __name__ == '__main__':
    RunCommand(True)
