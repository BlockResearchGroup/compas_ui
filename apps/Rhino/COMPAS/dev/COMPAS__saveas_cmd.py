from compas_ui.ui import UI


__commandname__ = "COMPAS__saveas"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.saveas()


if __name__ == "__main__":
    RunCommand(True)
