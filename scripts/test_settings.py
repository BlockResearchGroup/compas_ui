from compas.colors import Color
from compas_ui.rhino.forms import SettingsForm

SETTINGS = {
    "layer": "FF",
    "show.vertices:free": False,  # is this relevant?
    "show.vertices:is_anchor": True,  # is this relevant?
    "show.edges": True,
    "show.faces": False,
    "show.faces:all": False,  # is this relevant?
    "show.reactions": True,
    "show.loads": True,
    "show.pipes:forcedensities": False,
    "show.pipes:forces": True,
    "show.constraints": True,
    "color.vertices": Color.white(),
    "color.vertices:is_anchor": Color.red(),
    "color.vertices:is_fixed": Color.blue(),
    "color.vertices:is_constrained": Color.cyan(),
    "color.edges": Color.black(),
    "color.faces": Color.white().darkened(25),
    "color.tension": Color.red(),
    "color.compression": Color.blue(),
    "color.reactions": Color.green().darkened(50),
    "color.loads": Color.green().darkened(75),
    "color.invalid": Color.grey(),
    "color.pipes": Color.white().darkened(50),
    "scale.externalforces": 0.300,
    "pipe_thickness.min": 0.0,
    "pipe_thickness.max": 10.0,
    "tol.externalforces": 1e-3,
}

SettingsForm(SETTINGS).show()