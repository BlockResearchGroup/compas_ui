__commandname__ = "COMPAS__init"


def RunCommand(is_interactive):
    import json
    from compas_ui.ui import UI

    CONFIG = json.load("config.json")

    UI.reset()
    ui = UI(name=CONFIG["plugin"]["title"], settings=CONFIG["settings"])
    ui.scene_clear()


if __name__ == "__main__":
    RunCommand(True)
