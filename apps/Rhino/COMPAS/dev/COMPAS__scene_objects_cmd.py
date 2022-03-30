__commandname__ = "COMPAS__scene_objects"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.scene_objects()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
