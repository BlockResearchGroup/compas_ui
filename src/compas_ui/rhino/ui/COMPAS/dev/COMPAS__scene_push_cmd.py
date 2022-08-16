from compas_ui.ui import UI

# TODO: clarify intensions (speckle seems too dev for now)
# TODO: move to dev branch


__commandname__ = "COMPAS__scene_push"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.scene.speckle_push()


if __name__ == "__main__":
    RunCommand(True)
