from compas_ui.ui import UI


__commandname__ = "COMPAS__scene_update"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.scene_update()


if __name__ == "__main__":
    RunCommand(True)
