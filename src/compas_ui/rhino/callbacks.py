import scriptcontext as sc


def register_callback(callback):
    if callback.__name__ not in sc.sticky:
        sc.sticky[callback.__name__] = True
        sc.doc.ReplaceRhinoObject += callback
