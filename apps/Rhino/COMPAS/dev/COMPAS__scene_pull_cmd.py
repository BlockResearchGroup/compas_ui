__commandname__ = "COMPAS__scene_pull"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.proxy.project_from_speckle(ui)


if __name__ == "__main__":
    RunCommand(True)
