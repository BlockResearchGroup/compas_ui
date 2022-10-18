from compas_ui.ui import UI
from compas.datastructures import Mesh
from compas.geometry import Translation
import compas


ui = UI({"plugin": {"title": ["Hierrachy"]}, "settings": {}})
ui.scene.clear()

mesh1 = Mesh.from_obj(compas.get("faces.obj"))
mesh2 = Mesh.from_obj(compas.get("faces.obj"))
mesh2.transform(Translation.from_vector([15, 0, 0]))

obj1 = ui.scene.add(mesh1, name="mesh1")
obj2 = obj1.add(mesh2, name="mesh2")

ui.scene.update()
ui.scene_objects()
