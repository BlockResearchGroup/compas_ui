from compas_ui.ui import UI


__commandname__ = "COMPAS_scene_update"


@UI.error()
@UI.rhino_undo(__commandname__)
def RunCommand(is_interactive):

    ui = UI()
    ui.scene_update()


if __name__ == "__main__":
    RunCommand(True)
