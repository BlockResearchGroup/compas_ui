from compas_ui.values import IntValue
from compas_ui.values import BoolValue
from compas_ui.values import StrValue
from compas_ui.values import FloatValue
from compas_ui.values import ColorValue
from compas_ui.values import Settings

settings = Settings(
    {
        "a": IntValue(1),
        "b": BoolValue(True),
        "c": ColorValue((1, 0, 0)),
        "d.x": FloatValue(0.001),
        "d.y": StrValue("text"),
        "d.z.i": IntValue(1),
        "d.z.j": BoolValue(True),
    }
)

print(settings.value)

# group recursively based on the dot notation
def group(settings):
    groups = {}
    for key, value in settings.items():
        parts = key.split(".")
        if len(parts) > 1:
            if parts[0] not in groups:
                groups[parts[0]] = {}
            subkey = ".".join(parts[1:])
            groups[parts[0]][subkey] = value
        else:
            groups[key] = value

    for key, value in groups.items():
        if isinstance(value, dict):
            groups[key] = group(value)

    return groups


groups = group(settings.value)
print(groups)

settings.copy()
