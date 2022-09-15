import os
import json

from compas_ui.ui import UI
from compas_ui.rhino.forms import SplashForm


__commandname__ = "COMPAS_init"


HERE = os.path.dirname(__file__)
SPLASH = os.path.join(HERE, "assets", "index.html")

with open(os.path.join(HERE, "config.json")) as f:
    CONFIG = json.load(f)


@UI.error()
def RunCommand(is_interactive):

    UI.reset()
    ui = UI(config=CONFIG)
    ui.scene_clear()

    browser = SplashForm(title=ui.name, url=SPLASH)
    browser.show()


if __name__ == "__main__":
    RunCommand(True)
