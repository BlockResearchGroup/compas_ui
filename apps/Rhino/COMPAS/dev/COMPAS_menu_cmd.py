from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.rhino.forms import MenuForm
from compas_ui.rhino.forms import error
import os


__commandname__ = "COMPAS_menu"

HERE = os.path.dirname(__file__)

@error()
def RunCommand(is_interactive):

    m = MenuForm()
    m.load_config(HERE)
    m.show()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
