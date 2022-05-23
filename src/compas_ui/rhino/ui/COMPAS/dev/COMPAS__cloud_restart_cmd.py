from compas_ui.ui import UI


__commandname__ = "COMPAS__cloud_restart"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.cloud_restart()


if __name__ == "__main__":
    RunCommand(True)
