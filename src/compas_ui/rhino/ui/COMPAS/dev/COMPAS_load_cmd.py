from compas_ui.ui import UI


__commandname__ = "COMPAS_load"


@UI.error()
@UI.rhino_undo(__commandname__)
def RunCommand(is_interactive):
    ui = UI()
    ui.load()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
