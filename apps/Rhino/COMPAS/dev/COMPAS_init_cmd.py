from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import __plugin__ as PLUGIN

import os
from compas_ui.app import App
from compas_ui.rhino.forms import BrowserForm
from compas_ui.rhino.forms import error

SPLASH = os.path.join(os.path.dirname(__file__), 'splash', 'index.html')


__commandname__ = 'COMPAS_init'


@error()
def RunCommand(is_interactive):

    App.reset()

    # this should become part of the App
    # e.g. App.splash()
    browser = BrowserForm(title=PLUGIN.title, url=SPLASH)
    browser.show()

    app = App(name=PLUGIN.title, settings=PLUGIN.settings)
    app.scene.clear()


if __name__ == '__main__':
    RunCommand(True)
