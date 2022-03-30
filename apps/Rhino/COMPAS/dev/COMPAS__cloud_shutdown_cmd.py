__commandname__ = "COMPAS__cloud_shutdown"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.cloud_shutdown()


if __name__ == "__main__":
    RunCommand(True)
