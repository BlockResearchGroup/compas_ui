from compas_ui.ui import UI

# TODO: clarify intentions (speckle streams are too much of a dev thing for now)
# TODO: move to dev branch


__commandname__ = "COMPAS__scene_load"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    stream_id = ui.get_string(message="Stream id:")
    ui.scene.stream_id = stream_id
    ui.scene.speckle_pull()


if __name__ == "__main__":
    RunCommand(True)
