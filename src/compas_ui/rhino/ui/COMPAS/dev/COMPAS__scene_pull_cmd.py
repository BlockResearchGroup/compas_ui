from compas_ui.ui import UI


__commandname__ = "COMPAS__scene_pull"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.scene.speckle_pull()


if __name__ == "__main__":
    RunCommand(True)
