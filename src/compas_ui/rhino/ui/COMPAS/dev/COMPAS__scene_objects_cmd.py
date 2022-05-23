from compas_ui.ui import UI


__commandname__ = "COMPAS__scene_objects"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.scene_objects()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
