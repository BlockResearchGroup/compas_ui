from compas.plugins import plugin
import compas_rhino


@plugin(category='ui', requires=['Rhino'])
def get_real(message=None, default=None, minimum=None, maximum=None):
    return compas_rhino.rs.GetReal(message=message, number=default, minimum=minimum, maximum=maximum)
