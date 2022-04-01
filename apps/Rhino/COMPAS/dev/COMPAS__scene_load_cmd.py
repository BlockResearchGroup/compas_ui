__commandname__ = "COMPAS__scene_load"


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    ui = UI()
    stream_id = ui.get_string(message="Stream id:")
    ui.scene.stream_id = stream_id
    ui.scene.speckle_pull()


if __name__ == "__main__":
    RunCommand(True)
