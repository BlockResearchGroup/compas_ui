from compas_ui.ui import UI

# TODO: turn off recording for now


__commandname__ = "COMPAS_load"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.load()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
