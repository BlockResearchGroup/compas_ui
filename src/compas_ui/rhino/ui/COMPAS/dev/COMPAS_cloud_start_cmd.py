from compas_ui.ui import UI


__commandname__ = "COMPAS_cloud_start"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.cloud_start()


if __name__ == "__main__":
    RunCommand(True)
