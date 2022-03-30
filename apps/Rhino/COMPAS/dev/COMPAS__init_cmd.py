import os
import json

__commandname__ = "COMPAS__init"

HERE = os.path.dirname(__file__)
SPLASH = os.path.join(HERE, "assets", "index.html")

with open(os.path.join(HERE, "config.json")) as f:
    CONFIG = json.load(f)


def RunCommand(is_interactive):
    try:
        import compas  # noqa : F401
        import compas_rhino  # noqa : F401
        import compas_ui  # noqa : F401
        import compas_cloud  # noqa : F401

    except ImportError as e:
        print(e)

        import Rhino
        import Rhino.UI
        import Eto.Drawing
        import Eto.Forms

        info = """
To use COMPAS UI, following packages have to be available.

- compas
- compas_rhino
- compas_ui
- compas_cloud

Please activate and install an environment from the command line with at least these packages:

conda activate <environment name>
python -m compas_rhino.install

Use the editable flag for a dev install:

conda activate <environment name>
python -m compas_rhino.install --editable
"""

        class SetupDialog(Eto.Forms.Dialog[bool]):
            def __init__(self, info, title="Info"):
                self.Title = title
                self.Padding = Eto.Drawing.Padding(0)
                self.Resizable = False
                self.ClientSize = Eto.Drawing.Size(960, 540)
                textarea = Eto.Forms.TextArea()
                textarea.ReadOnly = True
                textarea.Text = info
                layout = Eto.Forms.DynamicLayout()
                layout.BeginVertical(
                    Eto.Drawing.Padding(12, 12, 12, 0),
                    Eto.Drawing.Size(0, 0),
                    True,
                    True,
                )
                layout.AddRow(textarea)
                layout.EndVertical()
                layout.BeginVertical(
                    Eto.Drawing.Padding(12, 12, 12, 18),
                    Eto.Drawing.Size(6, 0),
                    False,
                    False,
                )
                self.DefaultButton = Eto.Forms.Button(Text="OK")
                self.AbortButton = Eto.Forms.Button(Text="Cancel")
                self.DefaultButton.Click += self.ok
                self.AbortButton.Click += self.cancel
                layout.AddRow(None, self.DefaultButton, self.AbortButton)
                layout.EndVertical()
                self.Content = layout

            def ok(self, sender, event):
                self.Close(True)

            def cancel(self, sender, event):
                self.Close(False)

        dialog = SetupDialog(info)
        dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

    else:
        from compas_ui.ui import UI

        UI.reset()
        ui = UI(config=CONFIG)
        ui.splash(url=SPLASH)
        ui.scene_clear()


if __name__ == "__main__":
    RunCommand(True)
