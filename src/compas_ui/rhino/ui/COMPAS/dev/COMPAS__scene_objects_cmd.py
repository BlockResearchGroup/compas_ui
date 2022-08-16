from compas_ui.ui import UI

# TODO: turn off recording for now
# TODO: add namespace per plugin
# TODO: root objects under namespaces
# TODO: provide COMPAS as default namespace
# TODO: links instead of buttons?


__commandname__ = "COMPAS__scene_objects"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.scene_objects()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
