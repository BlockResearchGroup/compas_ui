from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas.datastructures import Mesh
from compas_ui.app import App
from compas_ui.rhino.forms import error


__commandname__ = 'COMPAS_test_mesh'


@error()
def RunCommand(is_interactive):

    app = App()

    mesh = Mesh.from_obj(compas.get('tubemesh.obj'))
    mesh.name = 'TubeMesh'

    app.scene.add(mesh)
    app.scene.update()
    app.record()


if __name__ == '__main__':
    RunCommand(True)
