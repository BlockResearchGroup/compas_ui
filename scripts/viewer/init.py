from compas.datastructures import Mesh
from compas_ui.app import App

app = App('FoFin', context='Viewer')

app.app.button(text="Mesh from meshgrid")
def mesh_from_meshgrid():
    dx = app.ui.get_real(parent=app.app.window, message='dx', default=10, minimum=1, maximum=100)
    dy = app.ui.get_real(parent=app.app.window, message='dy', default=10, minimum=1, maximum=100)
    mesh = Mesh.from_meshgrid(dx=dx, nx=10, dy=dy, ny=10)
    node = self.app.scene.add(mesh)
    print(node.color)
    self.app.scene.update()
    self.app.session.data['mesh'] = mesh

app.show()
