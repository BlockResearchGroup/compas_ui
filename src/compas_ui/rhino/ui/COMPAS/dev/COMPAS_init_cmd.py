import os
import json

from compas_ui.ui import UI

# TODO: auto start the cloud
# TODO: change splash screen
# TODO: check why loading takes so long
# TODO: check if current environment has compas_ui


__commandname__ = "COMPAS_init"


HERE = os.path.dirname(__file__)
SPLASH = os.path.join(HERE, "assets", "index.html")

with open(os.path.join(HERE, "config.json")) as f:
    CONFIG = json.load(f)


@UI.error()
def RunCommand(is_interactive):

    UI.reset()
    ui = UI(config=CONFIG)
    ui.splash(url=SPLASH)
    ui.scene_clear()


if __name__ == "__main__":
    RunCommand(True)
