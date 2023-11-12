from compas_ui.ui import UI
from compas_ui.rhino.forms import SettingsForm


__commandname__ = "COMPAS_settings"


@UI.error()
@UI.rhino_undo(__commandname__)
def RunCommand(is_interactive):
    ui = UI()

    form = SettingsForm(ui.registry, use_tab=True)
    if form.show():
        ui.registry.update(form.settings)

    ui.record()


if __name__ == "__main__":
    RunCommand(True)
