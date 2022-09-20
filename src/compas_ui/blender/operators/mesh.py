import os
import bpy  # noqa: E402

from compas.datastructures import Mesh
from compas_ui.ui import UI  # noqa: E402


class MeshCreateOperator(bpy.types.Operator):
    bl_idname = "compas.mesh_create"
    bl_label = "Save"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")  # noqa: F821

    def execute(self, context):
        ui = UI()
        path = self.filepath
        basename = os.path.basename(path)
        _, ext = os.path.splitext(path)

        # # this could be stored in blend data
        # self.ui.registry["mesh_create.FromFile.dirname"] = dirname

        if ext == ".obj":
            mesh = Mesh.from_obj(path)
        elif ext == ".off":
            mesh = Mesh.from_off(path)
        elif ext == ".ply":
            mesh = Mesh.from_ply(path)
        elif ext == ".json":
            mesh = Mesh.from_json(path)
        else:
            raise NotImplementedError

        mesh.name = basename

        # name = ui.get_string("Mesh name?", default=mesh.name)
        # if not name:
        #     name = mesh.name

        objects = ui.scene.get(mesh.name)
        if objects:
            for obj in objects:
                ui.scene.remove(obj)

        ui.scene.add(mesh, name=mesh.name)
        ui.scene.update()
        ui.record()

        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}
