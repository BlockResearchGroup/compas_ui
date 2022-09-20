from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Eto.Drawing as drawing
import Eto.Forms as forms
import Rhino.UI

import importlib
import sys


class ToolbarForm(forms.Form):
    def setup(self, toolbar, UI_folder, title="Toolbar"):
        sys.path.append(UI_folder)
        self.Owner = Rhino.UI.RhinoEtoApp.MainWindow
        self.Title = title
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(5, 5)
        layout.Padding = drawing.Padding(5)

        self.Content = forms.Scrollable()
        self.Content.Content = layout
        self.Padding = drawing.Padding(0)
        self.Resizable = False

        buttons = []
        for command in toolbar:
            if command.get("type") == "separator":
                label = forms.Label(Text="|")
                label.Font = drawing.Font("Arial", 20)
                label.TextColor = drawing.Color(0, 0, 0, 0.2)
                buttons.append(label)

            else:
                button = forms.Button()
                button.Size = drawing.Size(32, 32)
                icon = drawing.Icon(command["icon"])
                button.Image = icon.WithSize(32, 32)

                package = importlib.import_module("%s_cmd" % command["command"])

                def on_click(package):
                    def _on_click(sender, e):
                        package.RunCommand(True)

                    return _on_click

                button.Click += on_click(package)
                buttons.append(button)

        layout.AddRow(*buttons)
