__commandname__ = "COMPAS__project_pull"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.project.pull()


if __name__ == "__main__":
    RunCommand(True)
