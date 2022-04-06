__commandname__ = "COMPAS__scene_push"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.proxy.project_to_speckle(ui)


if __name__ == "__main__":
    RunCommand(True)
