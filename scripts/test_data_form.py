from compas.datastructures import Mesh
from compas_ui.rhino.forms import MeshDataForm
import compas

mesh = Mesh.from_obj(compas.get('faces.obj'))
MeshDataForm(mesh).show()