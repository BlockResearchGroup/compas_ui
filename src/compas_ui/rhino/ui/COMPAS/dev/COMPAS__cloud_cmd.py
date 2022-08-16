from compas_ui.ui import UI

# TODO: popup window with cloud controls and info (combination of start/restart, shutdown)


__commandname__ = "COMPAS__cloud"


@UI.error()
def RunCommand(is_interactive):

    pass


if __name__ == "__main__":
    RunCommand(True)
