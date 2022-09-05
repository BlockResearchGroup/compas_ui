from compas_ui.ui import UI
from compas_ui.rhino.forms import SettingsForm


__commandname__ = "COMPAS_settings"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    form = SettingsForm(ui.settings)
    if form.show():
        ui.settings.update(form.settings)


if __name__ == "__main__":
    RunCommand(True)
