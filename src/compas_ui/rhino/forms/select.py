from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ast import literal_eval

import Rhino
import Rhino.UI
import Eto.Drawing
import Eto.Forms


class ListSelectForm(Eto.Forms.Dialog[bool]):

    def __init__(self, items, title="Options"):
        self.items = items

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = False
        # self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        # self.ClientSize = Eto.Drawing.Size(width, height)

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(
            Eto.Drawing.Padding(0, 0, 0, 0), Eto.Drawing.Size(0, 0), True, True
        )
        layout.AddRow(box)
        layout.EndVertical()
        layout.BeginVertical(
            Eto.Drawing.Padding(12, 18, 12, 24), Eto.Drawing.Size(6, 0), False, False
        )
        layout.AddRow(None, self.ok, self.cancel)
        layout.EndVertical()

        self.Content = layout

    @property
    def ok(self):
        self.DefaultButton = Eto.Forms.Button(Text="OK")
        self.DefaultButton.Click += self.on_ok
        return self.DefaultButton

    @property
    def cancel(self):
        self.AbortButton = Eto.Forms.Button(Text="Cancel")
        self.AbortButton.Click += self.on_cancel
        return self.AbortButton

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        self._settings = settings.copy()
        self._names = names = sorted(settings.keys())
        self._values = [str(settings[name]) for name in names]

    @property
    def names(self):
        return self._names

    @property
    def values(self):
        return self._values

    def on_ok(self, sender, event):
        """Callback for the OK event."""
        try:
            for i, name in enumerate(self.names):
                value = self.table.DataStore[i][1]
                try:
                    value = literal_eval(value)
                except (TypeError, ValueError, SyntaxError):
                    pass
                self._settings[name] = value
        except Exception as e:
            print(e)
            self.Close(False)
        self.Close(True)

    def on_cancel(self, sender, event):
        """Callback for the CANCEL event."""
        self.Close(False)

    def show(self):
        """Show the form dialog."""
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
