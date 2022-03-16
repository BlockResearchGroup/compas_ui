from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from __plugin__ import settings

import os
from compas_ui.app import App
from compas_ui.rhino.forms.browser import BrowserForm

SPLASH = os.path.join(os.path.dirname(__file__), 'splash', 'index.html')


__commandname__ = 'COMPAS_init'


def RunCommand(is_interactive):

    App._instances = {}

    browser = BrowserForm(title='COMPAS', url=SPLASH)
    browser.show()

    app = App(name='COMPAS', settings=settings)
    app.scene.clear()


if __name__ == '__main__':
    RunCommand(True)
