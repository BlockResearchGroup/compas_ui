__commandname__ = "COMPAS__settings"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.update_settings()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
