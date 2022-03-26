__commandname__ = "COMPAS__saveas"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.saveas()


if __name__ == "__main__":
    RunCommand(True)
