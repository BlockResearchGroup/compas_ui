from compas_ui.ui import UI


__commandname__ = "COMPAS_scene_objects"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.scene_objects()


if __name__ == "__main__":
    RunCommand(True)
