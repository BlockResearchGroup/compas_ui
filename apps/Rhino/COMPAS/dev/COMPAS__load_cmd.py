__commandname__ = "COMPAS__load"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.load()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
