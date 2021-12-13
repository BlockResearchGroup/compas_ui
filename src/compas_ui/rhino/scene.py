import compas_rhino
from compas.plugins import plugin


@plugin(category='ui', requires=['Rhino'])
def update_scene(self):
    compas_rhino.rs.EnableRedraw(False)
    for guid in self.nodes:
        node = self.nodes[guid]
        node.draw()
    compas_rhino.rs.EnableRedraw(True)
    compas_rhino.rs.Redraw()


@plugin(category='ui', requires=['Rhino'])
def clear_scene(self):
    compas_rhino.rs.EnableRedraw(False)
    for guid in list(self.nodes):
        node = self.nodes[guid]
        node.clear()
        del self.nodes[guid]
    self.nodes = {}
    compas_rhino.rs.EnableRedraw(True)
    compas_rhino.rs.Redraw()
