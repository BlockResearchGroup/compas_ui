from compas_ui.ui import UI

# TODO: deactivate for now


__commandname__ = "COMPAS_redo"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.redo()


if __name__ == "__main__":
    RunCommand(True)