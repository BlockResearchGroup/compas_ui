__commandname__ = "COMPAS__scene_clear"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.scene_clear()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
