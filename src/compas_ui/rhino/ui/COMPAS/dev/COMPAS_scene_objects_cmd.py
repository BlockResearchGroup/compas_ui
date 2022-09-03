from compas_ui.ui import UI

# TODO: add namespace per plugin
# TODO: root objects under namespaces
# TODO: provide COMPAS as default namespace
# TODO: links instead of buttons?


__commandname__ = "COMPAS_scene_objects"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    ui.scene_objects()


if __name__ == "__main__":
    RunCommand(True)
