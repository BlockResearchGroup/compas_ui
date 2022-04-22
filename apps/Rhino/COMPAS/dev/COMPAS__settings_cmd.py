from compas_ui.ui import UI


__commandname__ = "COMPAS__settings"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.update_settings()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
