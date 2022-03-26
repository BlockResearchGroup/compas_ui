__commandname__ = "COMPAS_mesh_create"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()

    ui.controller.mesh_create()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
