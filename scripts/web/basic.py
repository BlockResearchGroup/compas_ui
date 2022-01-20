import compas
from compas_ui.app import App
from compas.datastructures import Mesh

mesh = Mesh.from_obj(compas.get('faces.obj'))
app = App('', context='Web')

obj = app.scene.add(mesh)
print(obj)
app.start()