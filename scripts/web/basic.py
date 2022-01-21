import compas
from compas_ui.app import App
from compas.datastructures import Mesh

# mesh = Mesh.from_obj(compas.get('faces.obj'))
mesh = Mesh.from_ply(compas.get('bunny.ply'))
app = App('', context='Web')

obj = app.scene.add(mesh)
app.start()