# required by Rhino
id = "{6c18fcab-3ae5-4b03-b515-d33d8078b977}"
version = "0.0.1.0"
title = "COMPAS"

# use this to check if the correct env is active in Rhino
# tell user to activate this env if that is not the case
# or do this automatically somehow
env = "compas-dev"
# use this to verify if the necessary packages of the env are installed as well?
packages = []

# default plugin settings
settings = {
    "text": "text",
    "int": 1,
    "float": 1.0,
    "bool": True,
    "color": (1.0, 0, 0),
    "dict": {
            "subtext": "text",
            "subint": 1,
            "subfloat": 1.0,
            "subbool": True,
            "subdict": {
                "subsubtext": "text",
            }
    }
}

# proxy info
