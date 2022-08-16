from compas_ui.ui import UI

# TODO: remove recoring for now
# TODO: develop settings object
# TODO: differentiate between clean and dirty settings
# TODO: only redraw if display settings are changed
# TODO: only do something if any of the settings is dirty


__commandname__ = "COMPAS__settings"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.update_settings()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
