from compas_ui.ui import UI
from compas.datastructures import Mesh
from compas.geometry import Translation
from compas_ui.objects.group import Group
import compas


ui = UI({"plugin": {"title": ["Group"]}, "settings": {}})
ui.scene.clear()

mesh1 = Mesh.from_obj(compas.get('faces.obj'))
mesh2 = mesh1.transformed(Translation.from_vector([15, 0, 0]))
mesh3 = mesh1.transformed(Translation.from_vector([0, 15, 0]))
mesh4 = mesh1.transformed(Translation.from_vector([15, 15, 0]))

group1 = ui.scene.add([], name='group1')
obj1 = group1.add(mesh1, name='mesh1')
obj2 = group1.add(mesh2, name='mesh2')

group2 = ui.scene.add([mesh3, mesh4], name='group2')

ui.scene.update()
ui.scene_objects()
