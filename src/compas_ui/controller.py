from compas.artists import Artist
from compas.datastructures import Mesh


class Controller(object):

    def __init__(self, app):
        self.app = app

    @property
    def view(self):
        return self.app.view

    def view_front(self):
        pass

    def view_right(self):
        pass

    def view_top(self):
        pass

    def view_perspective(self):
        pass

    def view_redraw(self):
        pass

    def view_clear(self):
        pass

    def display_wireframe(self):
        pass

    def display_shaded(self, use_lights=False):
        pass

    def diplay_ghosted(self):
        pass

    # -------------------------------------------------------------------------
    # Test
    # -------------------------------------------------------------------------

    def mesh_from_meshgrid(self):
        dx = self.app.ui.get_real(parent=self.app, message='dx', default=10, minimum=1, maximum=100)
        dy = self.app.ui.get_real(parent=self.app, message='dy', default=10, minimum=1, maximum=100)
        mesh = Mesh.from_meshgrid(dx=dx, nx=10, dy=dy, ny=10)
        node = self.app.scene.add(mesh)
        print(node.color)
        self.app.scene.update()
        self.app.session.data['mesh'] = mesh
