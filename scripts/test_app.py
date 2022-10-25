import time
import compas
import compas_rhino
from compas.datastructures import Mesh
from compas.geometry import Point
from compas_ui.app import App


compas_rhino.clear()

app = App(name="UITest")
app.scene.clear()

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
mesh.name = "TubeMesh"

obj = app.scene.add(mesh)
app.scene.update()
app.record()

time.sleep(1)

x, y, z = mesh.centroid()
obj.location = Point(-x, -y, 0)
app.scene.update()
app.record()

time.sleep(1)

app.undo()
app.save()
