from compas_ui.ui import UI


__commandname__ = "COMPAS_mesh_create"


@UI.error()
@UI.rhino_undo(__commandname__)
def RunCommand(is_interactive):
    ui = UI()
    ui.controller.mesh_create()


if __name__ == "__main__":
    RunCommand(True)
