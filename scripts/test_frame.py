from compas_ui.ui import UI
from compas.datastructures import Mesh
from compas.geometry import Frame
from compas_ui.objects import Group
import compas


ui = UI({"plugin": {"title": ["Frame"]}, "settings": {}})
ui.scene.clear()

mesh1 = Mesh.from_obj(compas.get('faces.obj'))
mesh2 = mesh1.copy()
mesh3 = mesh1.copy()

mesh1Obj = ui.scene.add(mesh1, name='mesh1')
mesh2Obj = mesh1Obj.add(mesh2, name='mesh2', frame=Frame([20, 0, 0], [1, 0, 0], [0, 1, 0]))
mesh2Obj.add(mesh3, name='mesh3', frame=Frame([0, 20, 0], [0, 0, 1], [0, 1, 0]))

ui.scene.update()
ui.scene_objects()
