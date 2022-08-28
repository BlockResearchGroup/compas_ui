from compas_ui.ui import UI

# TODO: disable for now


__commandname__ = "COMPAS_undo"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.undo()


if __name__ == "__main__":
    RunCommand(True)
