import time
import compas
import compas_rhino
from compas.datastructures import Mesh
from compas.geometry import Point
from compas_ui.app import App


compas_rhino.clear()

app = App(name='COMPAS')
app.scene.clear()

mesh = Mesh.from_obj(compas.get('tubemesh.obj'))
mesh.name = 'TubeMesh'

obj = app.scene.add(mesh)
app.scene.update()
app.record()

x, y, z = mesh.centroid()
for i in range(10):
    obj.location = Point(-x/10, -y/10, 0)
    time.sleep(1)

time.sleep(1)
app.scene.update()
app.record()

time.sleep(1)
app.undo()

#app.record()
# app.data.save()
