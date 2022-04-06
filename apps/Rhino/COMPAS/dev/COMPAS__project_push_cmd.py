__commandname__ = "COMPAS__project_push"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    ui.project.push()


if __name__ == "__main__":
    RunCommand(True)
