from compas_ui.ui import UI


__commandname__ = "COMPAS__scene_push"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.scene.speckle_push()


if __name__ == "__main__":
    RunCommand(True)
