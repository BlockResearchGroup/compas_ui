__commandname__ = "COMPAS__about"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.about()


if __name__ == "__main__":
    RunCommand(True)
