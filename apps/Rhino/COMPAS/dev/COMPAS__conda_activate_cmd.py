__commandname__ = "COMPAS__conda_activate"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.conda_activate()


if __name__ == "__main__":
    RunCommand(True)
