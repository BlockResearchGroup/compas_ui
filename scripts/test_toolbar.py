from compas_ui.rhino.forms import ToolbarForm

toolbar = [
    {
        "command": "COMPAS_init",
        "icon": "/Users/lichen7/WORK/compas_ui/src/compas_ui/rhino/ui/COMPAS/dev/assets/favicon.ico",
    },
    {"type": "separator"},
    {
        "command": "COMPAS_save",
        "icon": "/Users/lichen7/WORK/compas_ui/src/compas_ui/rhino/ui/COMPAS/dev/assets/favicon.ico",
    },
    {
        "command": "COMPAS_load",
        "icon": "/Users/lichen7/WORK/compas_ui/src/compas_ui/rhino/ui/COMPAS/dev/assets/favicon.ico",
    },
]

form = ToolbarForm()
form.setup(
    toolbar,
    "/Users/lichen7/WORK/compas_ui/src/compas_ui/rhino/ui/COMPAS/dev",
    title="COMPAS",
)
form.Show()
