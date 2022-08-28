from compas_ui.ui import UI


__commandname__ = "COMPAS_save"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.save()


if __name__ == "__main__":
    RunCommand(True)
