from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ast import literal_eval

import clr

clr.AddReference("Eto")
clr.AddReference("Rhino.UI")

import Rhino  # noqa : E402
import Rhino.UI  # noqa : E402
import Eto.Drawing  # noqa : E402
import Eto.Forms  # noqa : E402


class SettingsForm(Eto.Forms.Dialog[bool]):
    def __init__(self, settings, title="Settings", width=500, height=800):
        self._settings = None
        self._names = None
        self._values = None
        self.settings = settings

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)

        self.table = table = Eto.Forms.GridView()
        table.ShowHeader = True
        table.DataStore = [
            [name, value] for name, value in zip(self.names, self.values)
        ]

        c1 = Eto.Forms.GridColumn()
        c1.HeaderText = "Name"
        c1.Editable = False
        c1.DataCell = Eto.Forms.TextBoxCell(0)
        table.Columns.Add(c1)

        c2 = Eto.Forms.GridColumn()
        c2.HeaderText = "Value"
        c2.Editable = True
        c2.DataCell = Eto.Forms.TextBoxCell(1)
        table.Columns.Add(c2)

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(
            Eto.Drawing.Padding(0, 0, 0, 0), Eto.Drawing.Size(0, 0), True, True
        )
        layout.AddRow(table)
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
