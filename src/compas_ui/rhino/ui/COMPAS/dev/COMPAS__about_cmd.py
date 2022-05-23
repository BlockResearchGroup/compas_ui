from compas_ui.ui import UI


__commandname__ = "COMPAS__about"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.about()


if __name__ == "__main__":
    RunCommand(True)
