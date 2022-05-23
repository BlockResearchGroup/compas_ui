from compas_ui.ui import UI


__commandname__ = "COMPAS__conda_envs"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.conda_envs()


if __name__ == "__main__":
    RunCommand(True)
