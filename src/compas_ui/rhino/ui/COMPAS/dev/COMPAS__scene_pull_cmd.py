from compas_ui.ui import UI

# TODO: clarify intensions (speckle seems too dev for now)
# TODO: clarify difference with load
# TODO: move to dev branch


__commandname__ = "COMPAS__scene_pull"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.scene.speckle_pull()


if __name__ == "__main__":
    RunCommand(True)
