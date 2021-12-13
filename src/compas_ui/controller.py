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
        mesh = Mesh.from_meshgrid(dx=10, nx=10)
        self.app.scene.add(mesh)
        self.app.scene.update()
        self.app.session.data['mesh'] = mesh
