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

    ui = UI()  # noqa: F841

    config = [
        {
            "command": "COMPAS_load",
            "icon": os.path.join(HERE, "assets", "COMPAS_load.png"),
        },
        {
            "command": "COMPAS_saveas",
            "icon": os.path.join(HERE, "assets", "COMPAS_save.png"),
        },
        {"type": "separator"},
        {
            "command": "COMPAS_undo",
            "icon": os.path.join(HERE, "assets", "COMPAS_undo.png"),
        },
        {
            "command": "COMPAS_redo",
            "icon": os.path.join(HERE, "assets", "COMPAS_redo.png"),
        },
        {"type": "separator"},
        {
            "command": "COMPAS_scene_objects",
            "icon": os.path.join(HERE, "assets", "COMPAS_scene-objects.png"),
        },
        {
            "command": "COMPAS_scene_update",
            "icon": os.path.join(HERE, "assets", "COMPAS_scene-update.png"),
        },
        {
            "command": "COMPAS_scene_clear",
            "icon": os.path.join(HERE, "assets", "COMPAS_scene-clear.png"),
        },
        {"type": "separator"},
        {
            "command": "COMPAS_cloud_start",
            "icon": os.path.join(HERE, "assets", "COMPAS_cloud-start.png"),
        },
        {
            "command": "COMPAS_cloud_restart",
            "icon": os.path.join(HERE, "assets", "COMPAS_cloud-restart.png"),
        },
        {
            "command": "COMPAS_cloud_shutdown",
            "icon": os.path.join(HERE, "assets", "COMPAS_cloud-shutdown.png"),
        },
    ]

    toolbar = ToolbarForm()
    toolbar.setup(config, HERE, title="COMPAS")
    toolbar.Show()


if __name__ == "__main__":
    RunCommand(True)
