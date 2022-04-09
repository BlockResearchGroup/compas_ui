__commandname__ = "COMPAS__scene_pull"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.scene.speckle_pull()


if __name__ == "__main__":
    RunCommand(True)
