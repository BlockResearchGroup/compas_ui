import os
import json

__commandname__ = "COMPAS__init"


HERE = os.path.dirname(__file__)
SPLASH = os.path.join(HERE, "assets", "index.html")

with open(os.path.join(HERE, "config.json")) as f:
    CONFIG = json.load(f)


def RunCommand(is_interactive):
    from compas_ui.ui import UI

    UI.reset()
    ui = UI(config=CONFIG)
    ui.splash(url=SPLASH)
    ui.scene_clear()


if __name__ == "__main__":
    RunCommand(True)
