from compas_ui.ui import UI
from compas.datastructures import Mesh
from compas.geometry import Translation
from compas_ui.objects.group import Group
import compas


ui = UI({"plugin": {"title": ["Group"]}, "settings": {}})
ui.scene.clear()

mesh1 = Mesh.from_obj(compas.get('faces.obj'))
mesh2 = Mesh.from_obj(compas.get('faces.obj'))
mesh2.transform(Translation.from_vector([15, 0, 0]))



group = ui.scene.add([], name='group')
obj1 = group.add(mesh1, name='mesh1')
obj2 = group.add(mesh2, name='mesh2')

ui.scene.update()
ui.scene_objects()
