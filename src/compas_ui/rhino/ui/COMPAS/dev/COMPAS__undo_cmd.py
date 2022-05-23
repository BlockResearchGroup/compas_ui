from compas_ui.ui import UI


__commandname__ = "COMPAS__undo"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.undo()


if __name__ == "__main__":
    RunCommand(True)
