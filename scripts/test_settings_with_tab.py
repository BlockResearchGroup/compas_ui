from compas.colors import Color
from compas_ui.rhino.forms import SettingsForm

SETTINGS = {
    "plugin_a": {
        "color": Color.blue(),
        "int": 1,
        "float": 0.1
    },
    "plugin_b": {
        "bool": True,
        "text": "text"
    }
}

# Create form with tabs on first level
form = SettingsForm(SETTINGS, title="With Tabs", use_tab=True)
if form.show():
    print(form.settings)

# Create form without tabs
form = SettingsForm(SETTINGS, title="Without Tabs")
if form.show():
    print(form.settings)
