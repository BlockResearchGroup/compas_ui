from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino


class CommandMenu(object):
    def __init__(self, menu):
        self.menu = menu

    def select_action(self):
        def _select(message, options):
            if not options:
                return
            names = [option["name"] for option in options]
            name = compas_rhino.rs.GetString(message, names[0], names)
            if not name:
                return
            if name not in names:
                raise Exception("This option is not valid: {}".format(name))
            for option in options:
                if option["name"] == name:
                    break
            if "action" in option:
                return option

            message = option["message"]
            options = option.get("options")

            return _select(message, options)

        return _select(self.menu["message"], self.menu["options"])


class CommandAction(object):
    def __init__(self, name, action):
        self.name = name
        self.action = action

    def __call__(self, *args, **kwargs):
        return self.action(*args, **kwargs)
