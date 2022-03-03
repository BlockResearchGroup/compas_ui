import compas_rhino
from compas.plugins import plugin


@plugin(category='ui', requires=['Rhino'])
def update_scene(self):
    compas_rhino.rs.EnableRedraw(False)
    for guid in self.objects:
        obj = self.app.session['objects'][guid]
        obj.draw()
    compas_rhino.rs.EnableRedraw(True)
    compas_rhino.rs.Redraw()


@plugin(category='ui', requires=['Rhino'])
def clear_scene(self):
    compas_rhino.rs.EnableRedraw(False)
    for guid in self.objects:
        obj = self.app.session['objects'][guid]
        obj.clear()
    self.objects = set()
    compas_rhino.rs.EnableRedraw(True)
    compas_rhino.rs.Redraw()
