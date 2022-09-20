bl_info = {
    "name": "COMPAS",
    "blender": (2, 93, 0),
    "category": "Object",
    "version": (0, 1, 0),
    "author": "Tom Van Mele",
    "description": "COMPAS User Interface for Blender.",
    # "location": "",
    # "warning": "",
    # "doc_url": "",
    # "tracker_url": "",
    # "support": "COMMUNITY",
}

import bpy  # noqa: E402
from bpy.app.handlers import persistent  # noqa: E402

import compas  # noqa: E402

from compas_ui.ui import UI  # noqa: E402
from compas_ui.blender.operators import MeshCreateOperator  # noqa: E402


class SaveOperator(bpy.types.Operator):
    bl_idname = "compas.save"
    bl_label = "Save"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")  # noqa: F821

    def execute(self, context):
        self.report({"INFO"}, f"save at: {self.filepath}")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class LoadOperator(bpy.types.Operator):
    bl_idname = "compas.load"
    bl_label = "Load"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")  # noqa: F821

    def execute(self, context):
        ui = UI()
        ui.scene.clear()
        ui.state = compas.json_load(self.filepath)
        ui.scene.update()
        ui.record()
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class COMPASMain(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_main"
    bl_label = "COMPAS"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "COMPAS"

    def draw(self, context):
        col = self.layout.column()
        col.operator("compas.save", text="Save")
        col.operator("compas.load", text="Load")
        col.operator("compas.mesh_create", text="Mesh Create")


CLASSES = [
    COMPASMain,
    SaveOperator,
    LoadOperator,
    MeshCreateOperator,
]


@persistent
def init(*args):
    print("init")
    UI.reset()
    ui = UI(config={"plugin": {"title": "COMPAS"}, "settings": {}})
    ui.scene_clear()


def register():
    print("registered")
    for c in CLASSES:
        bpy.utils.register_class(c)

    bpy.app.handlers.load_post.append(init)


def unregister():
    print("unregistered")
    for c in CLASSES:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
