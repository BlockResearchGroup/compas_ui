from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
from compas_ui.ui import UI
from compas_ui.rhino.forms import ToolbarForm


__commandname__ = "COMPAS_toolbar"


HERE = os.path.dirname(__file__)


@UI.error()
def RunCommand(is_interactive):

    config = [
        {
            "command": "COMPAS_load",
            "icon": os.path.join(HERE, "assets", "COMPAS_load.png"),
        },
        {
            "command": "COMPAS_save",
            "icon": os.path.join(HERE, "assets", "COMPAS_save.png"),
        },
        {
            "command": "COMPAS_undo",
            "icon": os.path.join(HERE, "assets", "COMPAS_undo.png"),
        },
        {
            "command": "COMPAS_redo",
            "icon": os.path.join(HERE, "assets", "COMPAS_redo.png"),
        },
    ]

    toolbar = ToolbarForm()
    toolbar.setup(config, HERE, title="COMPAS")
    toolbar.Show()


if __name__ == "__main__":
    RunCommand(True)
