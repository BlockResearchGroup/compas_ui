__commandname__ = "COMPAS__cloud_start"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.cloud_start()


if __name__ == "__main__":
    RunCommand(True)
